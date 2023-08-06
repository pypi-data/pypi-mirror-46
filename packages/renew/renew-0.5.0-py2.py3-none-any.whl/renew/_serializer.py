import codecs
import contextlib
import importlib
import os
import re
import sys

from renew import _py_lang


def write_file(output_file_path, content, makedirs=False):
    parent_dir = os.path.dirname(output_file_path)

    if makedirs:
        if not os.path.isdir(parent_dir):
            assert not os.path.exists(parent_dir), "Path for parent dir already taken: %r." % parent_dir
            os.makedirs(parent_dir)
    else:
        if not os.path.isdir(parent_dir):
            raise ValueError("Target dir does not exist: {!r}.".format(parent_dir))

    with codecs.open(output_file_path, 'w', encoding="utf-8") as f:
        return f.write(content)


def _import_from_path(path_to_py_module):
    if not isinstance(path_to_py_module, str):
        raise TypeError("Expecting path to be a string.")

    if os.path.exists(path_to_py_module):
        import_dir_path, package_name = _split_path_and_name(path_to_py_module)
        with _supplementing_sys_path(import_dir_path):
            try:
                return importlib.import_module(package_name)
            except ImportError:
                return


def _split_path_and_name(python_file_path):
    import_dir_path, module_name = os.path.split(os.path.abspath(python_file_path))

    module_name = re.sub(r"(.*)\.pyc?$", r"\1", module_name)
    if module_name == "__init__":
        import_dir_path, module_name = os.path.split(import_dir_path)

    return import_dir_path, module_name


@contextlib.contextmanager
def _supplementing_sys_path(path_to_supplement):
    assert os.path.isdir(path_to_supplement), "Path has to be an existing dir: %s." % path_to_supplement

    if path_to_supplement in sys.path:
        yield
    else:
        sys.path.insert(0, path_to_supplement)
        try:
            yield
        finally:
            if path_to_supplement in sys.path:
                sys.path.pop(sys.path.index(path_to_supplement))


class PyStorage(object):

    def __init__(self, storage_path):
        """ Passing: 'some/path_to/pkg_name' or 'some/path_to/pkg_name/__init__.py' will cause:
        - pkg_name being a name of the package with 'some/path_to/pkg_name/__init__.py' as main file
        - 'some/path_to' appearing in sys.path for importing reasons
        - creating sub files in 'some/path_to/pkg_name/' directory
        """
        self.storage_path = storage_path
        self.load_from_disk()

    def load_from_disk(self):
        package = _import_from_path(self.storage_path)

        for name, proxy in self._collect_serializables():
            if package and hasattr(package, name):
                value_from_a_package = getattr(package, name)
                setattr(self, name, value_from_a_package)
            else:
                # cause a RAII case - single acquisition initializes the object
                getattr(self, name)

    @contextlib.contextmanager
    def updating_db(self):
        try:
            yield self
        finally:
            self.store_to_disk()

    def store_to_disk(self):
        labels, references = self._split_references()
        labels = {n: self._get_instance_obj(n) for n in labels}
        references = {n: id(self._get_instance_obj(n)) for n in references}

        self._dump_package_init(labels, references)
        for local_label_name in references:
            item = (local_label_name, self._get_instance_obj(local_label_name))
            content = _py_lang.build_py_file_content((item,))
            target_path = self._sub_module_path(local_label_name)
            write_file(target_path, content, makedirs=True)

    def _dump_package_init(self, labels, references):
        items = sorted(labels.items())
        rd = [(self._ref_module_name(n), n, id_) for n, id_ in references.items()]
        content = _py_lang.build_py_file_content(items, reference_deps=rd)
        target_path = self._sub_module_path("__init__")

        return write_file(target_path, content, makedirs=True)

    def __getattribute__(self, attribute_name):
        if attribute_name.startswith("_"):
            return object.__getattribute__(self, attribute_name)

        if attribute_name not in dir(self):
            msg = "{!r} object has no {!r} attribute."
            raise AttributeError(msg.format(self.__class__.__name__, attribute_name))

        attribute = object.__getattribute__(self, attribute_name)

        if isinstance(attribute, Label):
            hidden_name = self._hiding_attr_name(attribute_name)
            if not hasattr(self, hidden_name):
                setattr(self, hidden_name, attribute.default_constructor())
            return object.__getattribute__(self, hidden_name)

        return attribute

    def __setattr__(self, attribute_name, value):
        if attribute_name.startswith("_"):
            return object.__setattr__(self, attribute_name, value)

        if attribute_name in dir(self):
            attribute = object.__getattribute__(self, attribute_name)

            if isinstance(attribute, Label):
                hidden_name = self._hiding_attr_name(attribute_name)
                if not isinstance(value, attribute.default_constructor):
                    msg = "Cannot assign a different type than %r, got %r."
                    raise AttributeError(msg % (attribute.default_constructor.__name__, type(value).__name__))
                return object.__setattr__(self, hidden_name, value)

        return object.__setattr__(self, attribute_name, value)

    def _collect_serializables(self):
        """ The gets Label and Reference descriptors, Note that the result is unordered."""
        for name in dir(self):
            if not name.startswith("_"):
                value = object.__getattribute__(self, name)
                if isinstance(value, Label):
                    yield name, value

    def _split_references(self):
        labels, references = {}, {}
        for name, proxy in self._collect_serializables():
            if isinstance(proxy, Reference):
                references[name] = proxy
            else:
                labels[name] = proxy
        return labels, references

    @staticmethod
    def _hiding_attr_name(name):
        if not name.startswith("_"):
            name = "_" + name
        return "{}_hidden".format(name)

    def _get_instance_obj(self, name):
        hideous_name = self._hiding_attr_name(name)
        return self.__getattribute__(hideous_name)

    @staticmethod
    def _ref_module_name(human_readable_reference_name):
        if not human_readable_reference_name.startswith("_"):
            human_readable_reference_name = "_" + human_readable_reference_name
        return "_sub" + human_readable_reference_name

    def _sub_module_path(self, sub_name):
        root, pkg_name = _split_path_and_name(self.storage_path)
        if not sub_name.startswith("__init__"):
            sub_name = self._ref_module_name(sub_name)
        if not sub_name.endswith(".py"):
            sub_name += ".py"

        return os.path.join(root, pkg_name, sub_name)


class Label(object):
    def __init__(self, default_constructor):
        self._validate_is_a_constructor(default_constructor)
        self.default_constructor = default_constructor

    @classmethod
    def _validate_is_a_constructor(cls, function):
        try:
            assert function() is not None, "It has to return something."
        except Exception as e:
            msg = "The object passed to %r class (type: %r) has to be a callable wih no args and return anything. " \
                  "Failed to call or get return value from %r. Got %s: %s"

            type_name = getattr(function, '__name__', repr(function))
            raise TypeError(msg % (cls.__name__, type_name, function, type(e).__name__, e))


class Reference(Label):
    pass
