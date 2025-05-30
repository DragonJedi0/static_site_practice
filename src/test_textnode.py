import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_isText(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
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

    def test_empty_url(self):
        node = TextNode("The url is empty", TextType.LINK, None)
        node2 = TextNode("The url is empty", TextType.LINK, None)
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
        node = TextNode(None, TextType.TEXT)
        node2 = TextNode(None, TextType.TEXT)
        node_alt = TextNode("", TextType.TEXT)
        node_alt2 = TextNode("", TextType.TEXT)
        self.assertEqual(node, node2)
        self.assertEqual(node_alt, node_alt2)

    def test_texts(self):
        node = TextNode("This is the text of the nodes", TextType.TEXT)
        node2 = TextNode("This is the text of the nodes", TextType.TEXT)
        node_alt = TextNode("This is the text of the node_alt", TextType.TEXT)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node_alt)
        self.assertNotEqual(node, node_alt)

    # Test text_node_to_html_node()
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), 'This is a text node')

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<b>This is a text node</b>')

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<i>This is a text node</i>')

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<code>This is a text node</code>')

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": node.url})
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a text node</a>')

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertNotEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})
        self.assertEqual(html_node.to_html(), '<img src="https://www.example.com" alt="This is a text node"></img>')

    def test_invalid_type(self):
        node = TextNode("This is invalid", "Not a valid type")
        with self.assertRaises(Exception) as e:
            text_node_to_html_node(node)
        err_msg = e.exception
        self.assertEqual(str(err_msg), "Cannot Convert: Not a valid TextType")


if __name__ == "__main__":
    unittest.main()