import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_tags(self):
        node = LeafNode("p", "Hello World!")
        node2 = LeafNode("b", "Hello World!")
        node3 = LeafNode(None, "Hello World!")
        node4 = LeafNode("", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
        self.assertEqual(node2.to_html(), "<b>Hello World!</b>")
        self.assertEqual(node3.to_html(), "Hello World!")
        self.assertEqual(node4.to_html(), "Hello World!")

    def test_value(self):
        node = LeafNode("p", "Hello World!")
        node2 = LeafNode("p", "")
        node3 = LeafNode("p", None)
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")
        self.assertEqual(node2.to_html(), "<p></p>")
        with self.assertRaises(ValueError):
            node3.to_html()
    
    def test_props(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href":"https://www.google.com","target":"__blank"})
        node3 = LeafNode("a", "Click me!", {})
        node4 = LeafNode("a", "Click me!")
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com" target="__blank">Click me!</a>')
        self.assertEqual(node3.to_html(), '<a>Click me!</a>')
        self.assertEqual(node4.to_html(), '<a>Click me!</a>')
