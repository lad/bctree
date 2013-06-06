#!/usr/bin/env python

"""Some quick tests for BcTree using unittest.

Test classes are created dynamically to support parameterizing the
tests, see load_tests.
"""

from bctree import BcTree

import random
import unittest
from functools import partial
import os
import json


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

    def test_get_from(self):
        child = self.tree.get_from(self.add_path)
        self.assertTrue(child.value == self.add_path[-1])

    def test_get_from_none(self):
        path = self.add_path[:]
        path[-1] = str(random.random())
        child = self.tree.get_from(path)
        self.assertTrue(child == None)

    def test_add_child_entry(self):
        entry = self.Entry('one', 1, 2)
        self.tree.add(entry)
        self.assertTrue(self.tree.get('one').value is entry)

    def test_add_to_entry(self):
        entry = self.Entry('one', 1, 2)
        self.tree.add_to(self.add_path, entry)
        self.assertTrue(self.tree.find('one').value is entry)

    def test_extend(self):
        tree2 = BcTree(1)
        tree2.add(2)
        tree2.add(3).add(3.3)
        child = self.tree.get_from(self.add_path)

        expected = [l.value for l in child._children] + [l.value for l in tree2]

        child.extend(tree2)
        self.assertTrue([e.value for e in child.iterate(root=False)] ==
                        expected)

    def test_move(self):
        if not self.add_path or len(self.add_path) < 3:
            return
        src = self.add_path[2]
        self.tree.move(self.tree.value, src)
        parent, child = self.tree._find(src, BcTree.DFS)
        self.assertTrue(parent == self.tree and child.value == src)

    def test_remove(self):
        if len(self.add_path) < 2:
            return

        val = self.add_path[1]
        self.tree.remove(val)
        self.assertTrue(self.tree.find(val) is None)

    def test_remove_all(self):
        for parent, child in self.tree._iterate(root=False, order=BcTree.BFS):
            if parent == self.tree:
                self.tree.remove(child.value)

        self.assertTrue(list(self.tree) == [self.tree])

    def test_remove_from(self):
        if len(self.add_path) < 2:
            return
        self.tree.remove_from(self.add_path)
        self.assertTrue(self.tree.find(self.add_path[-1]) is None)

    def test_remove_root(self):
        self.assertRaises(ValueError, self.tree.remove, self.tree.value)

    def test_eq_root(self):
        root = BcTree(self.tree.value)
        self.assertTrue(self.tree == root)

    def test_eq_not_root(self):
        node = BcTree(str(random.random()))
        self.assertTrue(self.tree != node)

    def test_eq_child(self):
        if not self.dfs_values or len(self.dfs_values) < 2:
            return
        value = self.dfs_values[1]
        child = self.tree.get(value)
        self.assertTrue(child == BcTree(value))

    def test_find(self):
        for value in self.iter_values():
            self.assertTrue(self.tree.find(value) == BcTree(value))

    def test_find_none(self):
        self.assertTrue(self.tree.find(str(random.random())) is None)

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
    """Make a test with the given root and values."""
    tree = BcTree(root)
    for i in range(0, len(parents_values), 2):
        parent = parents_values[i]
        values = parents_values[i + 1]
        node = tree.find(parent)
        for value in values:
            node.add(value)
    return tree


def iter_values(root, values):
    """Yield the root and all values."""
    yield root
    for value in values:
        yield value


def parametrized_test_classes():
    """Generate test classes derived from unittest.TestCase.

    Different test parameters are setup as class data in each test
    class, effectively running the same tests with differing data.
    """
    with open(os.path.join(os.path.dirname(__file__), 'input.json')) as fd:
        testdict = json.load(fd)
        for name, value in testdict.iteritems():
            yield type('{}.TestBcTree'.format(name),
                       (TestBcTree, unittest.TestCase),
                       {'make_tree': partial(make_tree, value['root'],
                                             value['add_values']),
                       'iter_values': partial(iter_values, value['root'],
                                              value['dfs']),
                       'dfs_values': value['dfs'],
                       'bfs_values': value['bfs'],
                       'add_path': value['add_path']})


def load_tests(loader, tests, pattern):
    """Load dynamically created test classes."""
    suite = unittest.TestSuite()
    for cls in parametrized_test_classes():
        tests = loader.loadTestsFromTestCase(cls)
        suite.addTests(tests)
    return suite
