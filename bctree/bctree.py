#!/usr/bin/env python

"""BeatCleaver Unsorted Tree Implementation."""

from collections import deque


class BcTree(object):
    """Unsorted Native Python Tree."""

    DFS = 0
    BFS = 1

    def __init__(self, value=None):
        self.value = value
        self._children = []

    def __eq__(self, other):
        """Equality relies upon matching values only not children."""
        return isinstance(other, BcTree) and self.value == other.value

    # Check for existings/add replace? arg
    def add(self, value):
        """Add the given value as an immediate child."""
        child = BcTree(value)
        self._children.append(child)
        return child

    def get(self, value):
        """Get the immediate child that matches the given value."""
        if self.value == value:
            return self
        for child in self._children:
            if child.value == value:
                return child
        return None

    # pylint: disable-msg=W0212
    # pylint can't figure out that we're accessing a protected member
    # of our own class.
    def add_to(self, parent_values, value):
        """Add a value using a list of values as a "path" to the parent node.

           The parent_values list is expected to be a "path" of values. The
           value provided will be added to the last node in the parent list.
        """
        parent = self.get_from(parent_values)
        if parent:
            return parent.add(value)
        else:
            return None

    # pylint: disable-msg=W0212
    def get_from(self, values):
        """Get the node using the given value list."""
        if values[0] != self.value:
            return None

        cur = self
        for value in values[1:]:
            for child in cur._children:
                if child.value == value:
                    cur = child
                    break
            else:
                return None
        return cur

    def extend(self, tree):
        """Add the given tree as an immediate child."""
        self._children.append(tree)
        return tree

    def move(self, dst_value, src_value):
        if src_value == self.value:
            raise ValueError('Moving the root of the tree is not supported.')

        dst_node = self.find(dst_value)
        if not dst_node:
            raise ValueError('Source value "{}" not found in tree.'
                             .format(src_value))

        for parent, child in self._iterate(root=False):
            if child.value == src_value:
                break
        else:
            raise ValueError('Source value "{}" not found in tree.'
                             .format(src_value))

        parent._children.remove(child)
        dst_node._children.append(child)

    def remove(self):
        pass

    def find(self, value, order=DFS):
        """Find the given value in the tree using the given order."""
        if self.value == value:
            return self
        for tree in self.iterate(root=False, order=order):
            if tree.value == value:
                return tree
        return None

    def __iter__(self):
        """Iterate through the tree, depth first."""
        for _, child in self._iterate():
            yield child

    def iterate(self, root=True, order=DFS):
        """Iterate through the tree in the given order."""
        for _, child in self._iterate(root=root, order=order):
            yield child

    def _iterate(self, root=True, order=DFS):
        """Iterate through the tree yielding a tuple of (parent, child)"""
        if root:
            yield None, self

        to_visit = deque([(self, c) for c in self._children])
        if order == self.BFS:
            add_to_visit = to_visit.extend
        elif order == self.DFS:
            add_to_visit = lambda c: to_visit.extendleft(reversed(c))
        else:
            raise ValueError('Invalid "order" argument')

        while to_visit:
            parent, current = to_visit.popleft()
            yield parent, current
            add_to_visit([(current, c) for c in current._children])
