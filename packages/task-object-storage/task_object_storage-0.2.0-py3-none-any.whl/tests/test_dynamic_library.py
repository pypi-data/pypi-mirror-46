"""
Test dynamic library core.
"""
import pytest

from TOSLibrary.dynamic_library import DynamicLibrary


class Dummy:

    def _private(self):
        pass

    def method_without_args(self):
        return "Hello there"

    def method_with_arg(self, arg: int):
        return arg * 2

    def method_with_kwarg(self, arg: int, kwarg="just testing"):
        return kwarg

    def method_with_varargs(self, *args, **kwargs):
        return args

    def method_with_docstring(self):
        """Test docstring"""
        pass


@pytest.fixture
def library_class():
    class DummyLibrary(DynamicLibrary):
        def __init__(self):
            """Init docstring"""
            super(DummyLibrary, self).__init__()
            dummy = Dummy()
            self.add_component(dummy)

    return DummyLibrary


def test_add_component(library_class):
    """Test that after instantiating the class
    all new keywords appear as attributes."""
    lib = library_class()

    assert "method_without_args" not in dir(library_class)
    assert "method_with_arg" not in dir(library_class)

    assert "method_without_args" in dir(lib)
    assert "method_with_arg" in dir(lib)

    assert lib.method_without_args() == "Hello there"
    assert lib.method_with_arg(2) == 4


def test_get_keyword_names(library_class):
    lib = library_class()
    keywords = lib.get_keyword_names()

    assert "method_without_args" and "method_with_arg" in keywords


def test_run_keyword(library_class):
    lib = library_class()
    result1 = lib.run_keyword("method_without_args", (), {})
    result2 = lib.run_keyword("method_with_arg", (2,), {})

    assert result1 == "Hello there"
    assert result2 == 4


def test_get_attr_unknown_name(library_class):
    lib = library_class()
    with pytest.raises(AttributeError):
        lib.methodX()


def test_get_keyword_arguments(library_class):
    lib = library_class()
    expected = ["arg", "kwarg=just testing"]
    args = lib.get_keyword_arguments("method_with_kwarg")

    assert args == expected


def test_get_keyword_arguments_with_varargs(library_class):
    lib = library_class()
    expected = ["*args", "**kwargs"]
    args = lib.get_keyword_arguments("method_with_varargs")

    assert args == expected


def test_get_keyword_documentation(library_class):
    lib = library_class()
    expected = "Test docstring"
    doc = lib.get_keyword_documentation("method_with_docstring")

    assert doc == expected


def test_get_keyword_documentation_for_init(library_class):
    lib = library_class()
    expected = "Init docstring"
    doc = lib.get_keyword_documentation("__init__")

    assert doc == expected
