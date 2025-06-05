import unittest

from markdown_convert import markdown_to_blocks
from markdownblock import BlockType, block_to_block_type


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
