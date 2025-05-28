import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_isNormal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_isBold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_isItalic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_isCode(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_isLink(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_isImage(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_invalidType(self):
        with self.assertRaises(Exception):
            TextNode("Text Node has invalid type", "not a valid type")

    def test_empty_url(self):
        node = TextNode("The url is empty", TextType.LINK)
        node2 = TextNode("The url is empty", TextType.LINK)
        node_alt = TextNode("The url is blank", TextType.LINK, "")
        node_alt2 = TextNode("The url is blank", TextType.LINK, "")
        self.assertEqual(node, node2)
        self.assertEqual(node_alt, node_alt2)

    def test_urls(self):
        node = TextNode("This has a url", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This has a url", TextType.LINK, "https://www.boot.dev")
        node3 = TextNode("This doesn't have a URL", TextType.LINK)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)

    def test_empty_text(self):
        node = TextNode(None, TextType.NORMAL)
        node2 = TextNode(None, TextType.NORMAL)
        node_alt = TextNode("", TextType.NORMAL)
        node_alt2 = TextNode("", TextType.NORMAL)
        self.assertEqual(node, node2)
        self.assertEqual(node_alt, node_alt2)

    def test_texts(self):
        node = TextNode("This is the text of the nodes", TextType.NORMAL)
        node2 = TextNode("This is the text of the nodes", TextType.NORMAL)
        node_alt = TextNode("This is the text of the node_alt", TextType.NORMAL)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node_alt)
        self.assertNotEqual(node, node_alt)


if __name__ == "__main__":
    unittest.main()