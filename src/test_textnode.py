import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown_convert import *

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

    # Testing split_nodes_delimiter()
    def test_bold(self):
        node = TextNode("This text has a **bolded** word", TextType.TEXT)
        expected_list = [
            TextNode("This text has a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, expected_list)

    def test_italic(self):
        node = TextNode("This text has an _italicized_ word", TextType.TEXT)
        expected_list = [
            TextNode("This text has an ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(node_list, expected_list)

    def test_code(self):
        node = TextNode("This `code` is a test", TextType.TEXT)
        expected_list = [
            TextNode("This ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" is a test", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(node_list, expected_list)

    def test_multiline_code(self):
        node = TextNode("This code has multiple lines ```code\ncode\ncode```", TextType.TEXT)
        expected_list = [
            TextNode("This code has multiple lines ", TextType.TEXT),
            TextNode("code\ncode\ncode", TextType.CODE),
        ]
        node_list = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(node_list, expected_list)

    def test_mismatch(self):
        node = TextNode("This `code` is a test", TextType.TEXT)
        with self.assertRaises(TypeError):
            split_nodes_delimiter([node], "**", TextType.CODE)

    def test_bad_delimiter(self):
        node = TextNode("This `code is a test", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multi_delimiter(self):
        node = TextNode("This text has **two** bolded **words** here", TextType.TEXT)
        expected_list = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" bolded ", TextType.TEXT),
            TextNode("words", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, expected_list)

    def test_trailing_delimiter(self):
        node = TextNode("This text ends with a bolded **word**", TextType.TEXT)
        expected_list = [
            TextNode("This text ends with a bolded ", TextType.TEXT),
            TextNode("word", TextType.BOLD),
        ]
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, expected_list)

    def test_preceeding_delimiter(self):
        node = TextNode("**Shout** starts bolded", TextType.TEXT)
        expected_list = [
            TextNode("Shout", TextType.BOLD),
            TextNode(" starts bolded", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node_list, expected_list)

    def test_multi_node(self):
        node = TextNode("This text only has one **bolded** word", TextType.TEXT)
        node2 = TextNode("There is an empty bolded word at the end ****", TextType.TEXT)
        expected_list = [
            TextNode("This text only has one ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("There is an empty bolded word at the end ", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(node_list, expected_list)

    def test_multi_texttype(self):
        node_list = [
            TextNode("This text only has one _italicized_ word", TextType.TEXT),
            TextNode("These ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode("words", TextType.BOLD),
            TextNode(" have been preprocessed", TextType.TEXT),
        ]
        expected_list = [
            TextNode("This text only has one ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("These ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode("words", TextType.BOLD),
            TextNode(" have been preprocessed", TextType.TEXT),
        ]
        node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
        self.assertEqual(node_list, expected_list)

    # Testing extract_markdown_images()
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_match(self):
        matches = extract_markdown_images(
            "This is text with an ![image=https://i.imgur.com/zjjcJKZ.png]"
        )
        self.assertListEqual([], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "The first image is a ![elephant](https://elephant.img) and the second is a ![dog](https://dog.img)"
        )
        self.assertListEqual([
            ("elephant", "https://elephant.img"),
            ("dog", "https://dog.img"),
        ], matches)

    def test_no_image(self):
        matches = extract_markdown_images("Nothing here")
        self.assertListEqual([],matches)

    # Testing extract_markdown_links()
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_match(self):
        matches = extract_markdown_links(
            "This is text with a [link=https://i.imgur.com/zjjcJKZ.png]"
        )
        self.assertListEqual([], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "The first link is a [elephant](https://elephant.img) and the second is a [dog](https://dog.img)"
        )
        self.assertListEqual([
            ("elephant", "https://elephant.img"),
            ("dog", "https://dog.img"),
        ], matches)

    def test_no_link(self):
        matches = extract_markdown_links("Nothing here")
        self.assertListEqual([],matches)

    # Testing split_node_images
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_bad_images(self):
        node = TextNode(
            "This is text with an ![image=https://i.imgur.com/zjjcJKZ.png] and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image=https://i.imgur.com/zjjcJKZ.png] and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("This is text with an image and another second image", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual([TextNode("This is text with an image and another second image", TextType.TEXT)], new_nodes)

    def test_only_images(self):
        node = TextNode("![image1](https://i.imgur.com/123.png)![image2](https://i.imgur.com/456.png)", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/123.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/456.png"),
            ],
            new_nodes,
        )

    # Testing split_node_links
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_bad_links(self):
        node = TextNode(
            "This is text with a ![link](https://www.google.com) and another [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ![link](https://www.google.com) and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("This is text with a link and another link", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual([TextNode("This is text with a link and another link", TextType.TEXT)], new_nodes)

    def test_only_links(self):
        node = TextNode("[link1](https://www.google.com)[link2](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://www.google.com"),
                TextNode("link2", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_all_splits(self):
        text ="This sentence has all markdown types thus far. **Bolded** words. _Italics_. `Example Code`. An ![image](https://i.imgur.com/123.png), and a [link](https://www.google.com)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This sentence has all markdown types thus far. ", TextType.TEXT),
                TextNode("Bolded", TextType.BOLD),
                TextNode(" words. ", TextType.TEXT),
                TextNode("Italics", TextType.ITALIC),
                TextNode(". ", TextType.TEXT),
                TextNode("Example Code", TextType.CODE),
                TextNode(". An ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/123.png"),
                TextNode(", and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )
    
    def test_all_splits_partial_markdowns(self):
        text ="_This_ sentence has some markdown types thus far. ```Example\nCode```. A [link](https://www.google.com) that points to Google."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This", TextType.ITALIC),
                TextNode(" sentence has some markdown types thus far. ", TextType.TEXT),
                TextNode("Example\nCode", TextType.CODE),
                TextNode(". A ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" that points to Google.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_all_splits_no_markdowns(self):
        text ="This sentence is just text."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("This sentence is just text.", TextType.TEXT)], new_nodes,)

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blank_line_between_blocks(self):
        md = """
        This is **bolded** paragraph

        

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_bad_blocks(self):
        md = """
        This is **bolded** paragraph
        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line
        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertNotEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_blocks(self):
        md = """



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


if __name__ == "__main__":
    unittest.main()
