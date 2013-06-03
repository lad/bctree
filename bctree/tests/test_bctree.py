#!/usr/bin/env python

"""Some quick tests for BcTree using unittest.

There are classes created dynamically to support parameterizing the tests.
"""

from bctree import BcTree

import random
import unittest
from functools import partial


class TestBcTree(object):
    """Some basic tests for BcTree."""
    make_tree = None
    iter_values = None
    dfs_values = ()
    bfs_values = ()
    add_path = []

    class Entry(object):
        def __init__(self, name, a, b):
            self.name = name
            self.a, self.b = a, b

        def __eq__(self, other):
            return (isinstance(other, self.__class__) and
                    self.name == other.name) or \
                   (isinstance(other, str) and self.name == other)

    def setUp(self):
        self.tree = self.make_tree()

    def test_add_child(self):
        value = random.random()
        self.tree.add(value)
        self.assertTrue(self.tree.get(value).value == value)

    def test_add_to(self):
        value = str(random.random())
        self.tree.add_to(self.add_path, value)
        self.assertTrue(self.tree.find(value) == BcTree(value))

    def test_add_child_entry(self):
        entry = self.Entry('one', 1, 2)
        self.tree.add(entry)
        self.assertTrue(self.tree.get('one').value is entry)

    def test_add_to_entry(self):
        entry = self.Entry('one', 1, 2)
        self.tree.add_to(self.add_path, entry)
        self.assertTrue(self.tree.find('one').value is entry)

    def test_eq(self):
        tree2 = self.make_tree()
        self.assertTrue(self.tree == tree2)

    def test_find(self):
        for value in self.iter_values():
            self.assertTrue(self.tree.find(value) == BcTree(value))

    def test_find_none(self):
        self.assertTrue(self.tree.find(str(random.random())) == None)

    def test_iter(self):
        expected = [BcTree(value) for value in self.dfs_values]
        self.assertTrue(list(self.tree) == expected)

    def test_iterate_dfs_root(self):
        expected = [BcTree(value) for value in self.dfs_values]
        self.assertTrue(list(self.tree.iterate()) == expected)

    def test_iterate_bfs_root(self):
        expected = [BcTree(value) for value in self.bfs_values]
        self.assertTrue(list(self.tree.iterate(order=self.tree.BFS)) ==
                        expected)

    def test_iterate_dfs_no_root(self):
        expected = [BcTree(value) for value in self.dfs_values[1:]]
        self.assertTrue(list(self.tree.iterate(root=False)) == expected)

    def test_iterate_bfs_no_root(self):
        expected = [BcTree(value) for value in self.bfs_values[1:]]
        self.assertTrue(
                list(self.tree.iterate(order=self.tree.BFS, root=False)) ==
                expected)


def make_tree(root, parents_values):
    tree = BcTree(root)
    for parent, values in parents_values:
        node = tree.find(parent)
        for value in values:
            node.add(value)
    return tree


def iter_values(root, values):
    yield root
    for value in values:
        yield value


def parametrized_test_classes():
    """Generate test classes derived from unittest.TestCase.

    Different test parameters are setup as class data in each test
    class, effectively running the same tests with differing data.
    """
    params = (('root_only_none',            # name
                    None,                   # root value
                    (),                     # parents/values to add
                    [None],                 # Depth first search list
                    [None],                 # Breadth first search list
                    [None]),                # Path to add to
               ('root_only_value',
                   'root-value',
                   (),
                   ['root-value'],
                   ['root-value'],
                   ['root-value']),
               ('single',
                    'rootval',
                    (('rootval', ['a']),),
                    ['rootval', 'a'],
                    ['rootval', 'a'],
                    ['rootval', 'a']),
               ('onelevel',
                    None,
                    ((None, ['a', 'b', 'c', 'd']),),
                    [None, 'a', 'b', 'c', 'd'],
                    [None, 'a', 'b', 'c', 'd'],
                    [None, 'b']),
              ('twolevel',
                    'root',
                    (('root', ['a', 'b', 'c']),
                     ('a', ['a.1']),
                     ('b', ['b.1'])),
                    ['root', 'a', 'a.1', 'b', 'b.1', 'c'],
                    ['root', 'a', 'b', 'c', 'a.1', 'b.1'],
                    ['root', 'a', 'a.1']),
              ('threelevel',
                    'root',
                    (('root', ['a', 'b', 'c']),
                     ('a', ['a.1', 'a.2']),
                     ('b', ['b.1', 'b.2', 'b.3']),
                     ('b.2', ['b.2.1', 'b.2.2']),
                     ('b.3', ['b.3.1', 'b.3.2'])),
                    ['root', 'a', 'a.1', 'a.2', 'b', 'b.1', 'b.2', 'b.2.1',
                      'b.2.2', 'b.3', 'b.3.1', 'b.3.2', 'c'],
                    ['root', 'a', 'b', 'c', 'a.1', 'a.2', 'b.1', 'b.2', 'b.3',
                      'b.2.1', 'b.2.2', 'b.3.1', 'b.3.2'],
                    ['root', 'b', 'b.3', 'b.3.1']))
    for name, root, values, dfs, bfs, add_path in params:
        yield type('{}.TestBcTree'.format(name),
                   (TestBcTree, unittest.TestCase),
                   {'make_tree': partial(make_tree, root, values),
                    'iter_values': partial(iter_values, root, dfs),
                    'dfs_values': dfs,
                    'bfs_values': bfs,
                    'add_path': add_path})


def load_tests(loader, tests, pattern):
    """Load dynamically created test classes."""
    suite = unittest.TestSuite()
    for cls in parametrized_test_classes():
        tests = loader.loadTestsFromTestCase(cls)
        suite.addTests(tests)
    return suite
