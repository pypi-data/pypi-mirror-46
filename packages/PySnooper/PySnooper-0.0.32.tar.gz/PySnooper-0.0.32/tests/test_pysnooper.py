# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.

import io
import textwrap
import types

from python_toolbox import sys_tools, temp_file_tools
import pytest

import pysnooper
from pysnooper.variables import needs_parentheses
from .utils import (assert_output, VariableEntry, CallEntry, LineEntry,
                    ReturnEntry, OpcodeEntry, ReturnValueEntry, ExceptionEntry)


def test_string_io():
    string_io = io.StringIO()

    @pysnooper.snoop(string_io)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            VariableEntry('x', '7'),
            LineEntry('y = 8'),
            VariableEntry('y', '8'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
        )
    )



def test_callable():
    string_io = io.StringIO()

    def write(msg):
        string_io.write(msg)

    @pysnooper.snoop(write)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            VariableEntry('x', '7'),
            LineEntry('y = 8'),
            VariableEntry('y', '8'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
        )
    )



def test_watch():

    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @pysnooper.snoop(watch=(
            'foo.x',
            'io.__name__',
            'len(foo.__dict__["x"] * "abc")',
    ))
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('Foo'),
            VariableEntry('io.__name__', "'io'"),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo'),
            VariableEntry('foo.x', '2'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '6'),
            LineEntry(),
            VariableEntry('i', '0'),
            LineEntry(),
            VariableEntry('foo.x', '4'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '12'),
            LineEntry(),
            VariableEntry('i', '1'),
            LineEntry(),
            VariableEntry('foo.x', '16'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '48'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None')
        )
    )


def test_watch_explode():
    class Foo:
        def __init__(self, x, y):
            self.x = x
            self.y = y


    @pysnooper.snoop(watch_explode=('_d', '_point', 'lst + []'))
    def my_function():
        _d = {'a': 1, 'b': 2, 'c': 'ignore'}
        _point = Foo(x=3, y=4)
        lst = [7, 8, 9]
        lst.append(10)

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('Foo'),
            CallEntry('def my_function():'),
            LineEntry(),
            VariableEntry('_d'),
            VariableEntry("_d['a']", '1'),
            VariableEntry("_d['b']", '2'),
            VariableEntry("_d['c']", "'ignore'"),
            LineEntry(),
            VariableEntry('_point'),
            VariableEntry('_point.x', '3'),
            VariableEntry('_point.y', '4'),
            LineEntry(),
            VariableEntry('(lst + [])[0]', '7'),
            VariableEntry('(lst + [])[1]', '8'),
            VariableEntry('(lst + [])[2]', '9'),
            VariableEntry('lst'),
            VariableEntry('lst + []'),
            LineEntry(),
            VariableEntry('(lst + [])[3]', '10'),
            VariableEntry('lst'),
            VariableEntry('lst + []'),
            ReturnEntry(),
            ReturnValueEntry('None')
        )
    )


def test_variables_classes():
    class WithSlots(object):
        __slots__ = ('x', 'y')

        def __init__(self):
            self.x = 3
            self.y = 4

    @pysnooper.snoop(watch=(
            pysnooper.Keys('_d', exclude='c'),
            pysnooper.Attrs('_d'),  # doesn't have attributes
            pysnooper.Attrs('_s'),
            pysnooper.Indices('_lst')[-3:],
    ))
    def my_function():
        _d = {'a': 1, 'b': 2, 'c': 'ignore'}
        _s = WithSlots()
        _lst = list(range(1000))

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('WithSlots'),
            CallEntry('def my_function():'),
            LineEntry(),
            VariableEntry('_d'),
            VariableEntry("_d['a']", '1'),
            VariableEntry("_d['b']", '2'),
            LineEntry(),
            VariableEntry('_s'),
            VariableEntry('_s.x', '3'),
            VariableEntry('_s.y', '4'),
            LineEntry(),
            VariableEntry('_lst'),
            VariableEntry('_lst[997]', '997'),
            VariableEntry('_lst[998]', '998'),
            VariableEntry('_lst[999]', '999'),
            ReturnEntry(),
            ReturnValueEntry('None')
        )
    )



def test_single_watch_no_comma():

    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @pysnooper.snoop(watch='foo')
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('Foo'),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo'),
            LineEntry(),
            VariableEntry('i', '0'),
            LineEntry(),
            LineEntry(),
            VariableEntry('i', '1'),
            LineEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None')
        )
    )


def test_long_variable():
    @pysnooper.snoop()
    def my_function():
        foo = list(range(1000))
        return foo

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = my_function()
    assert result == list(range(1000))
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            CallEntry('def my_function():'),
            LineEntry('foo = list(range(1000))'),
            VariableEntry('foo', '[0, 1, 2, 3, 4, 5, ...]'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('[0, 1, 2, 3, 4, 5, ...]')
        )
    )


def test_repr_exception():
    class Bad(object):
        def __repr__(self):
            1 / 0

    @pysnooper.snoop()
    def my_function():
        bad = Bad()

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('Bad'),
            CallEntry('def my_function():'),
            LineEntry('bad = Bad()'),
            VariableEntry('bad', value_regex=r'<Bad instance at 0x\w+ \(__repr__ raised ZeroDivisionError\)>'),
            ReturnEntry(),
            ReturnValueEntry('None')
        )
    )


def test_depth():
    string_io = io.StringIO()

    def f4(x4):
        result4 = x4 * 2
        return result4

    def f3(x3):
        result3 = f4(x3)
        return result3

    def f2(x2):
        result2 = f3(x2)
        return result2

    @pysnooper.snoop(string_io, depth=3)
    def f1(x1):
        result1 = f2(x1)
        return result1

    result = f1(10)
    assert result == 20
    output = string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry(),
            VariableEntry(),
            CallEntry('def f1(x1):'),
            LineEntry(),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f2(x2):'),
            LineEntry(),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f3(x3):'),
            LineEntry(),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),
        )
    )


def test_method_and_prefix():
    class Baz(object):
        def __init__(self):
            self.x = 2

        @pysnooper.snoop(watch=('self.x',), prefix='ZZZ')
        def square(self):
            foo = 7
            self.x **= 2
            return self

    baz = Baz()

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = baz.square()
    assert result is baz
    assert result.x == 4
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('self', prefix='ZZZ'),
            VariableEntry('self.x', '2', prefix='ZZZ'),
            CallEntry('def square(self):', prefix='ZZZ'),
            LineEntry('foo = 7', prefix='ZZZ'),
            VariableEntry('foo', '7', prefix='ZZZ'),
            LineEntry('self.x **= 2', prefix='ZZZ'),
            VariableEntry('self.x', '4', prefix='ZZZ'),
            LineEntry(prefix='ZZZ'),
            ReturnEntry(prefix='ZZZ'),
            ReturnValueEntry(prefix='ZZZ'),
        ),
        prefix='ZZZ'
    )


def test_file_output():
    with temp_file_tools.create_temp_folder(prefix='pysnooper') as folder:
        path = folder / 'foo.log'

        @pysnooper.snoop(path)
        def my_function(_foo):
            x = 7
            y = 8
            return y + x

        result = my_function('baba')
        assert result == 15
        with path.open() as output_file:
            output = output_file.read()
        assert_output(
            output,
            (
                VariableEntry('_foo', value_regex="u?'baba'"),
                CallEntry('def my_function(_foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
            )
        )


def test_confusing_decorator_lines():
    string_io = io.StringIO()

    def empty_decorator(function):
        return function

    @empty_decorator
    @pysnooper.snoop(string_io,
                     depth=2)  # Multi-line decorator for extra confusion!
    @empty_decorator
    @empty_decorator
    def my_function(foo):
        x = lambda bar: 7
        y = 8
        return y + x(foo)

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry(),
            VariableEntry(),
            LineEntry(),
            VariableEntry(),
            LineEntry(),
            # inside lambda
            VariableEntry('bar', value_regex="u?'baba'"),
            CallEntry('x = lambda bar: 7'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('7'),
            # back in my_function
            ReturnEntry(),
            ReturnValueEntry('15'),
        )
    )


def test_lambda():
    string_io = io.StringIO()
    my_function = pysnooper.snoop(string_io)(lambda x: x ** 2)
    result = my_function(7)
    assert result == 49
    output = string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry('x', '7'),
            CallEntry(source_regex='^my_function = pysnooper.*'),
            LineEntry(source_regex='^my_function = pysnooper.*'),
            ReturnEntry(source_regex='^my_function = pysnooper.*'),
            ReturnValueEntry('49'),
        )
    )


def test_unavailable_source():
    with temp_file_tools.create_temp_folder(prefix='pysnooper') as folder, \
            sys_tools.TempSysPathAdder(str(folder)):
        module_name = 'iaerojajsijf'
        python_file_path = folder / ('%s.py' % (module_name,))
        content = textwrap.dedent(u'''
            import pysnooper
            @pysnooper.snoop()
            def f(x):
                return x
        ''')
        with python_file_path.open('w') as python_file:
            python_file.write(content)
        module = __import__(module_name)
        python_file_path.unlink()
        with sys_tools.OutputCapturer(stdout=False,
                                      stderr=True) as output_capturer:
            result = getattr(module, 'f')(7)
        assert result == 7
        output = output_capturer.output
        assert_output(
            output,
            (
                VariableEntry(stage='starting'),
                CallEntry('SOURCE IS UNAVAILABLE'),
                LineEntry('SOURCE IS UNAVAILABLE'),
                ReturnEntry('SOURCE IS UNAVAILABLE'),
                ReturnValueEntry('7'),
            )
        )


def test_no_overwrite_by_default():
    with temp_file_tools.create_temp_folder(prefix='pysnooper') as folder:
        path = folder / 'foo.log'
        with path.open('w') as output_file:
            output_file.write(u'lala')
        @pysnooper.snoop(str(path))
        def my_function(foo):
            x = 7
            y = 8
            return y + x
        result = my_function('baba')
        assert result == 15
        with path.open() as output_file:
            output = output_file.read()
        assert output.startswith('lala')
        shortened_output = output[4:]
        assert_output(
            shortened_output,
            (
                VariableEntry('foo', value_regex="u?'baba'"),
                CallEntry('def my_function(foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
            )
        )


def test_overwrite():
    with temp_file_tools.create_temp_folder(prefix='pysnooper') as folder:
        path = folder / 'foo.log'
        with path.open('w') as output_file:
            output_file.write(u'lala')
        @pysnooper.snoop(str(path), overwrite=True)
        def my_function(foo):
            x = 7
            y = 8
            return y + x
        result = my_function('baba')
        result = my_function('baba')
        assert result == 15
        with path.open() as output_file:
            output = output_file.read()
        assert 'lala' not in output
        assert_output(
            output,
            (
                VariableEntry('foo', value_regex="u?'baba'"),
                CallEntry('def my_function(foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),

                VariableEntry('foo', value_regex="u?'baba'"),
                CallEntry('def my_function(foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
            )
        )


def test_error_in_overwrite_argument():
    with temp_file_tools.create_temp_folder(prefix='pysnooper') as folder:
        with pytest.raises(Exception, match='can only be used when writing'):
            @pysnooper.snoop(overwrite=True)
            def my_function(foo):
                x = 7
                y = 8
                return y + x


def test_needs_parentheses():
    assert not needs_parentheses('x')
    assert not needs_parentheses('x.y')
    assert not needs_parentheses('x.y.z')
    assert not needs_parentheses('x.y.z[0]')
    assert not needs_parentheses('x.y.z[0]()')
    assert not needs_parentheses('x.y.z[0]()(3, 4 * 5)')
    assert not needs_parentheses('foo(x)')
    assert not needs_parentheses('foo(x+y)')
    assert not needs_parentheses('(x+y)')
    assert not needs_parentheses('[x+1 for x in ()]')
    assert needs_parentheses('x + y')
    assert needs_parentheses('x * y')
    assert needs_parentheses('x and y')
    assert needs_parentheses('x if z else y')


def test_with_block():
    # Testing that a single Tracer can handle many mixed uses
    snoop = pysnooper.snoop()

    def foo(x):
        if x == 0:
            bar1(x)
            qux()
            return

        with snoop:
            # There should be line entries for these three lines,
            # no line entries for anything else in this function,
            # but calls to all bar functions should be traced
            foo(x - 1)
            bar2(x)
            qux()
        int(4)
        bar3(9)
        return x

    @snoop
    def bar1(_x):
        qux()

    @snoop
    def bar2(_x):
        qux()

    @snoop
    def bar3(_x):
        qux()

    def qux():
        return 9  # not traced, mustn't show up

    with sys_tools.OutputCapturer(stdout=False,
                                  stderr=True) as output_capturer:
        result = foo(2)
    assert result == 2
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            # In first with
            VariableEntry('bar1'),
            VariableEntry('bar2'),
            VariableEntry('bar3'),
            VariableEntry('foo'),
            VariableEntry('qux'),
            VariableEntry('snoop'),
            VariableEntry('x', '2'),
            LineEntry('foo(x - 1)'),

            # In with in recursive call
            VariableEntry('bar1'),
            VariableEntry('bar2'),
            VariableEntry('bar3'),
            VariableEntry('foo'),
            VariableEntry('qux'),
            VariableEntry('snoop'),
            VariableEntry('x', '1'),
            LineEntry('foo(x - 1)'),

            # Call to bar1 from if block outside with
            VariableEntry('_x', '0'),
            VariableEntry('qux'),
            CallEntry('def bar1(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),

            # In with in recursive call
            LineEntry('bar2(x)'),

            # Call to bar2 from within with
            VariableEntry('_x', '1'),
            VariableEntry('qux'),
            CallEntry('def bar2(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),

            # In with in recursive call
            LineEntry('qux()'),

            # Call to bar3 from after with
            VariableEntry('_x', '9'),
            VariableEntry('qux'),
            CallEntry('def bar3(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),

            # -- Similar to previous few sections,
            # -- but from first call to foo

            # In with in first call
            LineEntry('bar2(x)'),

            # Call to bar2 from within with
            VariableEntry('_x', '2'),
            VariableEntry('qux'),
            CallEntry('def bar2(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),

            # In with in first call
            LineEntry('qux()'),

            # Call to bar3 from after with
            VariableEntry('_x', '9'),
            VariableEntry('qux'),
            CallEntry('def bar3(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
        ),
    )


def test_with_block_depth():
    string_io = io.StringIO()

    def f4(x4):
        result4 = x4 * 2
        return result4

    def f3(x3):
        result3 = f4(x3)
        return result3

    def f2(x2):
        result2 = f3(x2)
        return result2

    def f1(x1):
        str(3)
        with pysnooper.snoop(string_io, depth=3):
            result1 = f2(x1)
        return result1

    result = f1(10)
    assert result == 20
    output = string_io.getvalue()
    assert_output(
        output,
        (
            VariableEntry(),
            VariableEntry(),
            VariableEntry(),
            LineEntry('result1 = f2(x1)'),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f2(x2):'),
            LineEntry(),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f3(x3):'),
            LineEntry(),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),
        )
    )
