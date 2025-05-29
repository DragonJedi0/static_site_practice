import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("p", [grandchild_node])
        inner_parent = ParentNode("span", [child_node])
        inner_parent2 = ParentNode("span", [child_node])
        parent_node = ParentNode("div", [inner_parent, inner_parent2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandchild</b></p></span><span><p><b>grandchild</b></p></span></div>"
        )

    def test_to_html_empty_list(self):
        parent_node = ParentNode("div", [])
        parent_node2 = ParentNode("div", None)
        self.assertEqual(parent_node.to_html(), "<div></div>")
        with self.assertRaises(ValueError) as e:
            parent_node2.to_html()
            self.assertEqual(e, "HTMLNode list cannot be None or empty")

    def test_to_html_empty_tag(self):
        parent_node = ParentNode("", [])
        parent_node2 = ParentNode(None, [])
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
            self.assertEqual(e, "")
        with self.assertRaises(ValueError) as e:
            parent_node2.to_html()
            self.assertEqual(e, "HTMLNode list cannot be None or empty")

    def test_to_html_nested_children(self):
        nested_children = [
            LeafNode("p", "Some text"),
            LeafNode("b", "Bolded text"),
            LeafNode("i", "Italic text")
        ]
        parent_node = ParentNode("div", [nested_children])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Some text</p><b>Bolded text</b><i>Italic text</i></div>"
        )

    def test_to_html_nested_grandchildren(self):
        nested_children = [
            LeafNode(None, "Some text"),
            LeafNode("b", "Bolded text"),
            LeafNode("i", "Italic text")
        ]
        grandchild_node = ParentNode("p", [nested_children])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p>Some text<b>Bolded text</b><i>Italic text</i></p></span></div>"
        )