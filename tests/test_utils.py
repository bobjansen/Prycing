"""Test the failure modes of the utils functions."""
import unittest

from Prycing.options.utils import Tree

class TestTree(unittest.TestCase):
    """Test failure modes of the tree class."""
    def test_empty_tree(self):
        """Test that creating a tree of negative height raises."""
        self.assertRaises(
            ValueError,
            Tree, -1)

    def test_negative_level(self):
        """Test that getting a negative level raises."""
        tree = Tree(2)
        self.assertRaises(
            ValueError,
            tree.get_level, -1)

    def test_out_of_tree_level(self):
        """Test that getting a level outside of the tree raises."""
        tree = Tree(2)
        self.assertRaises(
            ValueError,
            tree.get_level, 3)

    def test_node_out_of_tree(self):
        """Test that getting a node outside of the tree raises."""
        tree = Tree(2)
        self.assertRaises(
            ValueError,
            tree.get_node, 1, 2)

    def test_set_node_out_of_tree(self):
        """Test that getting a node outside of the tree raises."""
        tree = Tree(2)
        self.assertRaises(
            ValueError,
            tree.set_node, 1, 2, 3)

    def test_tree_repr(self):
        """Test that getting a node outside of the tree raises."""
        tree = Tree(2)
        tree.set_node(0, 0, 1)
        tree.set_node(1, 0, 2)
        tree.set_node(1, 1, 3)
        self.assertEqual(
            repr(tree),
            "\n\n1\n3, 2")
