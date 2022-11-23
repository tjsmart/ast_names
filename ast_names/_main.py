from __future__ import annotations

import ast
import logging
from typing import Sequence


_logger = logging.getLogger(__package__)


def _collect_import_names(node: ast.Import | ast.ImportFrom) -> Sequence[str]:
    """
    Collect import names into a list and check whether an alias
    is being used instead.
    """
    x = []
    for name in node.names:
        if name.asname is None:
            x.append(name.name)
        else:
            x.append(name.asname)
    return x


class NameListener(ast.NodeVisitor):
    """
    Extends NodeVisitor to scan the top level ast for variable names.
    These variable names are collected into a set.

    Example:
    >>> import ast
    >>> tree = ast.parse('''
    ... import sys
    ... a = 1
    ... def foo():
    ...    pass
    ... ''')
    >>> listener = NameListener()
    >>> listener.visit(tree)
    >>> listener.names
    {'a', 'foo', 'sys'}
    """

    def __init__(self) -> None:
        self.names: set[str] = set()
        super().__init__()

    def visit_Import(self, node: ast.Import):
        names = _collect_import_names(node)
        _logger.info("Found Import: ", names, node.lineno)
        self.names.update(names)

    def visit_ImportFrom(self, node: ast.Import):
        names = _collect_import_names(node)
        _logger.info("Found ImportFrom: ", names, node.lineno)
        self.names.update(names)

    def visit_FunctionDef(self, node):
        _logger.info("Found Function: ", node.name, node.lineno)
        self.names.add(node.name)

    def visit_AsyncFunctionDef(self, node):
        _logger.info("Found AsyncFunction: ", node.name, node.lineno)
        self.names.add(node.name)

    def visit_ClassDef(self, node):
        _logger.info("Found Class: ", node.name, node.lineno)
        self.names.add(node.name)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            return
        if isinstance(node.ctx, ast.Del):
            _logger.info("Found Deleted Name: ", node.id, node.lineno)
            self.names.remove(node.id)
            return

        _logger.info("Found Name: ", node.id, node.lineno)
        self.names.add(node.id)


def ast_names(source: str | bytes) -> set[str]:
    """
    Collect the top level variable names using the ast.

    Args:
        source: Source python code.

    Returns:
        A set of variable names
    """
    tree = ast.parse(source)

    listener = NameListener()
    listener.visit(tree)

    return listener.names
