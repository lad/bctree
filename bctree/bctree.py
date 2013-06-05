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
        return self._get_from(values)[1]

    def _get_from(self, values):
        """Get the parent and the node using the given value list."""
        if values[0] != self.value:
            return None, None
        elif len(values) == 1:
            return None, self

        child = self
        for value in values[1:]:
            parent = child
            for child in parent._children:
                if child.value == value:
                    break
            else:
                return None, None

        return parent, child

    def extend(self, tree):
        """Add the given tree as an immediate child."""
        self._children.append(tree)
        return tree

    def move(self, dst_value, src_value, order=DFS):
        """Move a node and its decendents.

           The source and destination nodes are identified by their values
           only. A find operation is performed for both using the given
           order."""
        if src_value == self.value:
            raise ValueError('Moving the root of the tree is not supported.')

        dst_parent = self.find(dst_value, order=order)
        if not dst_parent:
            raise ValueError('Source value "{}" not found in tree.'
                             .format(src_value))

        src_parent, src = self._find(src_value, order=order)
        if not src_parent or not src:
            raise ValueError('Source value "{}" not found in tree.'
                             .format(src_value))

    def move_from(self, dst_parent_values, src_values):
        """Move a node and its decendents.

        The source and destination nodes are identified by a "path" of
        values from the root node to the desired node."""
        dst = self.get_from(dst_parent_values)
        if not dst:
            raise ValueError('Destination values ( {} ) not found in tree.'
                             .format(dst_parent_values))

        src_parent, src = self._get_from(src_values)
        if not src_parent or not src:
            raise ValueError('Source values ( {} ) not found in tree.'
                             .format(src_values))

        src_parent._children.remove(src)
        dst._children.add(src)

    def remove(self, value):
        """Remove the given value from the tree."""
        parent, child = self._find(value, self.DFS)
        if not parent or not child:
            raise ValueError('Value "{}" not found in tree.'.format(value))

        parent._children.remove(child)
        return child

    def remove_from(self, values):
        """Remove a value from the tree using a "path" of values."""
        parent, child = self._get_from
        if not parent or not child:
            raise ValueError('Values ( {} ) not found in tree.'
                             .format(values))
        parent._children.remove(child)

    def find(self, value, order=DFS):
        """Find the given value in the tree using the given order."""
        return self._find(value, order=order)[1]

    def _find(self, value, order):
        """Return parent and child for a matching child value."""
        if self.value == value:
            return None, self
        for parent, child in self._iterate(root=False, order=order):
            if child.value == value:
                return parent, child
        return None, None

    def __iter__(self):
        """Iterate through the tree, depth first."""
        for _, tree in self._iterate():
            yield tree

    def iterate(self, root=True, order=DFS):
        """Iterate through the tree in the given order."""
        for _, tree in self._iterate(root=root, order=order):
            yield tree

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
