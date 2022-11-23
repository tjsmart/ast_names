import pytest

from ast_names import ast_names


def example_source(source: str):
    def wrapper(fn):
        def closure(*args, **kwargs):
            return fn(source, *args, **kwargs)

        return closure

    return wrapper


@example_source(
    """\
bar()
x
3 * y
"""
)
def test_basic_expressions(source):
    assert ast_names(source) == set()


@example_source(
    """\
import sys
"""
)
def test_basic_import(source):
    assert ast_names(source) == {"sys"}


@example_source(
    """\
import sys, os
"""
)
def test_import_multi(source):
    assert ast_names(source) == {"sys", "os"}


@example_source(
    """\
import sys as foo
"""
)
def test_import_alias(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
from foo import bar
"""
)
def test_basic_fromimport(source):
    assert ast_names(source) == {"bar"}


@example_source(
    """\
from foo import (
    bar,
    baz,
)
"""
)
def test_fromimport_multi(source):
    assert ast_names(source) == {"bar", "baz"}


@example_source(
    """\
from foo import bar as baz
"""
)
def test_fromimport_alias(source):
    assert ast_names(source) == {"baz"}


@example_source(
    """\
def foo():
    ...
"""
)
def test_basic_function(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
def foo(x, y=10):
    ...
"""
)
def test_function_with_params(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
def foo():
    x = 10

    def bar():
        ...
"""
)
def test_function_with_locals(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
async def foo():
    ...
"""
)
def test_async_function(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
class Foo:
    ...
"""
)
def test_basic_class(source):
    assert ast_names(source) == {"Foo"}


@example_source(
    """\
class Foo(Bar, Baz):
    ...
"""
)
def test_class_with_parents(source):
    assert ast_names(source) == {"Foo"}


@example_source(
    """\
class Foo:
    x = 10
    def bar(self):
        y = 2
"""
)
def test_class_with_locals(source):
    assert ast_names(source) == {"Foo"}


@example_source(
    """\
foo = 1
"""
)
def test_basic_assignment(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
foo += 1
"""
)
def test_augmented_assignment(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
foo: int = 1
"""
)
def test_annotated_assignment(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
if (foo := bar()):
    ...

while (baz := bar()):
    ...
"""
)
def test_walrus_assignment(source):
    assert ast_names(source) == {"foo", "baz"}


@example_source(
    """\
for foo in bar:
    ...
"""
)
def test_forloop_assignment(source):
    assert ast_names(source) == {"foo"}


@example_source(
    """\
async for foo in bar:
    ...
"""
)
def test_async_forloop_assignment(source):
    assert ast_names(source) == {"foo"}


@pytest.mark.xfail(reason="comprehension value should not be usable outside of loop")
@example_source(
    """\
[foo for foo in bar]
"""
)
def test_comprehension_assignment(source):
    assert ast_names(source) == set()


@example_source(
    """\
if True:
    foo = 1
"""
)
def test_basic_if(source):
    assert ast_names(source) == {"foo"}


@pytest.mark.xfail(reason="truthy check not implemented")
@example_source(
    """\
if False:
    foo = 1
"""
)
def test_if_has_truthy_check(source):
    assert ast_names(source) == {}


@example_source(
    """\
with foo() as bar:
    ...
"""
)
def test_basic_with(source):
    assert ast_names(source) == {"bar"}


@example_source(
    """\
async with foo() as bar:
    ...
"""
)
def test_async_with(source):
    assert ast_names(source) == {"bar"}


@example_source(
    """\
x = 1
del x
"""
)
def test_basic_del(source):
    assert ast_names(source) == set()


@example_source(
    """\
x = 1
del x
x = 1
"""
)
def test_del_then_reassign(source):
    assert ast_names(source) == {"x"}


@pytest.mark.xfail(reason="No check for deleting of globals")
@example_source(
    """\
x = 1
def foo():
    global x
    del x
foo()
"""
)
def test_checks_deleting_of_globals(source):
    assert ast_names(source) == set()


@example_source(
    """\
import sys, os
import sys as foo

from foo import (
    bar as baz,
    alpha
)

def my_func():
    ...

class MyClass:
    ...

MYCONSTANT = 1
"""
)
def test_putting_it_all_together(source):
    assert ast_names(source) == {
        "sys",
        "os",
        "foo",
        "baz",
        "alpha",
        "my_func",
        "MyClass",
        "MYCONSTANT",
    }
