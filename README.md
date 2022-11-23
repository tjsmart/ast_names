# ast_names

Collect top level variable names using the ast.


## Installation

```
pip install ast_names
```

## Usage

```pycon
>>> from ast_names import ast_names
>>> ast_names("""
... import sys, os
... import sys as foo
...
... from foo import (
...     bar as baz,
...     alpha
... )
...
... MYCONSTANT = 1
...
... def my_func():
...     ...
...
... class MyClass:
...     ...
... """)
{'os', 'MYCONSTANT', 'alpha', 'baz', 'foo', 'sys', 'MyClass', 'my_func'}
```
