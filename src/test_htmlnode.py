import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("p", "This is not ready")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("a", "Click me!", None, {"href":"https://www.google.com"})
        node2 = HTMLNode("a", "Click me!", None, None)
        node3 = HTMLNode("a", "Click me!", None, "")
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
        self.assertEqual(node2.props_to_html(), '')
        self.assertEqual(node3.props_to_html(), '')

    def test_children_list(self):
        child = HTMLNode("p", "This is a paragraph")
        child2 = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com"})
        child3 = HTMLNode(None, "This is plain text")
        empty_child = HTMLNode()

        child_list = [child, child2, child3, empty_child]

        node = HTMLNode("div", None, child_list)
        node2 = HTMLNode("div", None)
        node3 = HTMLNode("div", None, [])
        self.assertEqual(node.children, child_list)
        self.assertNotEqual(node2.children, child_list)
        self.assertNotEqual(node3.children, child_list)
