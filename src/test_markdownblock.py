import unittest

from markdownblock import BlockType, block_to_block_type, markdown_to_html_node


class TestMarkDownBlock(unittest.TestCase):
    # Test Exception
    def test_no_markdown_block(self):
        empty = block_to_block_type("")
        self.assertEqual(BlockType.PARAGRAPH, empty)
        with self.assertRaises(Exception) as e:
            block_to_block_type(None)
        err_msg = e.exception
        self.assertEqual(str(err_msg), "Markdown block cannot be None")

    # Test block_to_block_type()
    def test_header(self):
        block_type1 = block_to_block_type("# This is a header level 1")
        block_type2 = block_to_block_type("## This is a header level 2")
        block_type3 = block_to_block_type("### This is a header level 3")
        block_type4 = block_to_block_type("#### This is a header level 4")
        block_type5 = block_to_block_type("##### This is a header level 5")
        block_type6 = block_to_block_type("###### This is a header level 6")
        self.assertEqual(BlockType.HEADING, block_type1)
        self.assertEqual(BlockType.HEADING, block_type2)
        self.assertEqual(BlockType.HEADING, block_type3)
        self.assertEqual(BlockType.HEADING, block_type4)
        self.assertEqual(BlockType.HEADING, block_type5)
        self.assertEqual(BlockType.HEADING, block_type6)

    def test_bad_header(self):
        header = block_to_block_type("####### This is not a header")
        self.assertNotEqual(BlockType.HEADING, header)
        self.assertEqual(BlockType.PARAGRAPH, header)

    def test_no_header(self):
        header = block_to_block_type("This is not a header")
        self.assertNotEqual(BlockType.HEADING, header)
        self.assertEqual(BlockType.PARAGRAPH, header)

    def test_code_block(self):
        code_block = "```\nExample Code\nNewLine\n```"
        block_type = block_to_block_type(code_block)
        self.assertEqual(BlockType.CODEBLOCK, block_type)

    def test_bad_code_block(self):
        code_block = block_to_block_type("```This is not an expected code block```")
        self.assertNotEqual(BlockType.CODEBLOCK, code_block)
        self.assertEqual(BlockType.PARAGRAPH, code_block)

    def test_no_code_block(self):
        code_block = block_to_block_type("This is not a code block")
        self.assertNotEqual(BlockType.CODEBLOCK, code_block)
        self.assertEqual(BlockType.PARAGRAPH, code_block)

    def test_quote_block(self):
        md = "> This is a single line quote block"
        md_alt = """> This is a quote block.
> You can tell it's a quote block because of the '>' at the begining of each line.
> Every line in a quote block has one."""
        quote_block = block_to_block_type(md)
        quote_block2 = block_to_block_type(md_alt)
        self.assertEqual(BlockType.QUOTE, quote_block)
        self.assertEqual(BlockType.QUOTE, quote_block2)

    def test_bad_quote_block(self):
        md = """> This is the first line
> This is the second line
But this last line isn't formatted correctly
"""
        quote_block = block_to_block_type(md)
        self.assertNotEqual(BlockType.QUOTE, quote_block)
        self.assertEqual(BlockType.PARAGRAPH, quote_block)

    def test_no_quote_block(self):
        md = """This is not a quote block\nThis is not a quote block"""
        quote_block = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, quote_block)

    def test_unordered_list(self):
        md = "- This list has one item"
        md_alt = """- This is an unordered list
- Every line begins with a dash
- But the order of the list is not organized"""
        unordered_list = block_to_block_type(md)
        unordered_list2 = block_to_block_type(md_alt)
        self.assertEqual(BlockType.UNORDERED, unordered_list)
        self.assertEqual(BlockType.UNORDERED, unordered_list2)

    def test_bad_unordered_list(self):
        md = """- This is an unordered list
- Every line begins with a dash
But the last line is not formatted correctly
"""
        unordered_list = block_to_block_type(md)
        self.assertNotEqual(BlockType.UNORDERED, unordered_list)
        self.assertEqual(BlockType.PARAGRAPH, unordered_list)

    def test_no_unordered_list(self):
        md = """This is not an unordered list\nThis is not an unordered list"""
        unordered_list = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, unordered_list)

    def test_ordered_list(self):
        md = "1. This list has one item"
        md_alt = """1. This is an ordered list
2. Every line begins with a number and a dot
3. But the order of the list is organized sequntially"""
        ordered_list = block_to_block_type(md)
        ordered_list2 = block_to_block_type(md_alt)
        self.assertEqual(BlockType.ORDERED, ordered_list)
        self.assertEqual(BlockType.ORDERED, ordered_list2)

    def test_bad_ordered_list(self):
        md = """1. This is an ordered list
2. Every line begins with a number and a dot
4. But the last line is not formatted correctly"""
        ordered_list = block_to_block_type(md)
        self.assertNotEqual(BlockType.ORDERED, ordered_list)
        self.assertEqual(BlockType.PARAGRAPH, ordered_list)

    # Test markdown_to_html_node()
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_paragraphs_with_urls(self):
        md = """
        This is a paragraph with a [link](https://google.com)
        to Google.

        This is a paragraph with an ![image](https://i.imgur/123.png)

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with a <a href="https://google.com">link</a> to Google.</p><p>This is a paragraph with an <img src="https://i.imgur/123.png" alt="image"></img></p></div>'
            )

    def test_combined_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        This is a paragraph with a [link](https://google.com)
        to Google.

        This is a paragraph with an ![image](https://i.imgur/123.png)

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><p>This is a paragraph with a <a href="https://google.com">link</a> to Google.</p><p>This is a paragraph with an <img src="https://i.imgur/123.png" alt="image"></img></p></div>'
            )

    def test_empty_paragraphs(self):
        md = """




        """
        node = markdown_to_html_node(md)
        node2 = markdown_to_html_node("")
        html = node.to_html()
        html2 = node2.to_html()
        self.assertEqual(html, "<div><p></p></div>")
        self.assertEqual(html2, "<div></div>")
        with self.assertRaises(Exception) as e:
            markdown_to_html_node(None)
        err_msg = e.exception
        self.assertEqual(str(err_msg), "no markdown text provided")

    def test_headings(self):
        md = """# This the main
        heading

        This is a paragraph

        ## This is a second heading

        This is the paragraph under the 2nd heading.

        ### This is a third heading

        This is the paragraph under the 3rd heading with a [link](https://www.google.com).

        #### This is a fourth heading

        This is the paragraph under the 4th heading.

        ##### This is a fifth heading

        This is the paragraph under the 5th heading with an _italic_ word.

        ###### This is a sixth heading

        This is the paragraph under the 6th heading with a **bold** word.
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>This the main heading</h1><p>This is a paragraph</p>" \
        "<h2>This is a second heading</h2><p>This is the paragraph under the 2nd heading.</p>" \
        '<h3>This is a third heading</h3><p>This is the paragraph under the 3rd heading with a <a href="https://www.google.com">link</a>.</p>' \
        "<h4>This is a fourth heading</h4><p>This is the paragraph under the 4th heading.</p>" \
        "<h5>This is a fifth heading</h5><p>This is the paragraph under the 5th heading with an <i>italic</i> word.</p>" \
        "<h6>This is a sixth heading</h6><p>This is the paragraph under the 6th heading with a <b>bold</b> word.</p></div>"
        self.assertEqual(html, expected)

    def test_bad_headings(self):
        md = """####### This heading should be a paragraph

        This is another paragraph

        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>####### This heading should be a paragraph</p><p>This is another paragraph</p></div>"
        )

    def test_quote_blocks(self):
        md = """## Quotes

        Quote blocks have the following rules

        > This is a quote block.
        > Every line should have a '>' at the begining.
        > After is a paragraph.

        This is the paragraph.
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Quotes</h2><p>Quote blocks have the following rules</p>" \
            "<blockquote>This is a quote block.\nEvery line should have a '>' at the begining.\nAfter is a paragraph.</blockquote>" \
            "<p>This is the paragraph.</p></div>"
        )

    def test_bad_quote_blocks(self):
        md = """> This is a quote block
        
        In this quote is a paragrah
        with a **bold** word
        
        > This is a second quote block
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>> This is a quote block  In this quote is a paragrah with a <b>bold</b> word  > This is a second quote block</p></div>"
        )

    def test_unordered_lists(self):
        md = """# Unordered Lists

        Unordered Lists have a '-' at the start of each line.

        - The order of the list is not displayed
        - It can be configured as a dot, square, or line
        - Numbers or letters are not considered unordered lists.
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Unordered Lists</h1><p>Unordered Lists have a '-' at the start of each line.</p><ul><li>The order of the list is not displayed</li>\n<li>It can be configured as a dot, square, or line</li>\n<li>Numbers or letters are not considered unordered lists.</li></ul></div>"
        )

    def test_bad_unordered_list(self):
        md = """- The order of the list is not displayed
        - It can be configured as a dot, square, or line
        Numbers or letters are not considered unordered lists.
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>- The order of the list is not displayed - It can be configured as a dot, square, or line Numbers or letters are not considered unordered lists.</p></div>"
        )

    def test_ordered_lists(self):
        md = """# Ordered Lists

        Ordered Lists have a number followed by a '.' and a space at the start of each line.

        1. The order of the list is displayed
        2. It can be configured as a number, letter, or roman numeral.
        3. Symbols are not considered ordered lists.
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><h1>Ordered Lists</h1><p>Ordered Lists have a number followed by a '.' and a space at the start of each line.</p><ol><li>The order of the list is displayed</li>\n<li>It can be configured as a number, letter, or roman numeral.</li>\n<li>Symbols are not considered ordered lists.</li></ol></div>"
        )

    def test_bad_ordered_lists(self):
        md = """1. The order of the list is displayed
        2. It can be configured as a number, letter, or roman numeral.
        4. Symbols are not considered ordered lists.
        
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><p>1. The order of the list is displayed 2. It can be configured as a number, letter, or roman numeral. 4. Symbols are not considered ordered lists.</p></div>"
        )

    def test_codeblocks(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        print("Expected:")
        print("<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
        print("Actual:")
        print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
