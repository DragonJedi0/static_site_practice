import re
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from markdown_convert import split_nodes_delimiter, markdown_to_blocks, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODEBLOCK = "code_block"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def block_to_block_type(block):
    if not block is None:
        lines = block.split("\n")

        if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
            return BlockType.CODEBLOCK
        if block.startswith(">"):
            for line in lines:
                if not line.startswith(">"):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        if block.startswith("- "):
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED
        if block.startswith("1. "):
            i = 1
            for line in lines:
                if not line.startswith(f"{i}. "):
                    return BlockType.PARAGRAPH
                i += 1
            return BlockType.ORDERED
        return BlockType.PARAGRAPH
    else:
        raise Exception("Markdown block cannot be None")

def markdown_to_html_node(markdown):
    child_nodes = []
    block_list = markdown_to_blocks(markdown)

    def decorate_header(text):
        text_list = text.split("\n")
        clean_text = " ".join(text_list)
        if clean_text.startswith("# "):
            tag = "h1"
        if clean_text.startswith("## "):
            tag = "h2"
        if clean_text.startswith("### "):
            tag = "h3"
        if clean_text.startswith("#### "):
            tag = "h4"
        if clean_text.startswith("##### "):
            tag = "h5"
        if clean_text.startswith("###### "):
            tag = "h6"
        clean_text = clean_text.lstrip("#")
        return LeafNode(tag, clean_text.strip())
    
    def text_to_child_node(text, block_type):
        if block_type is BlockType.PARAGRAPH:
            text_list = text.split("\n")
            clean_text = " ".join(text_list)
            child_node_list = text_to_textnodes(clean_text)
        else:
            child_node_list = text_to_textnodes(text)
        return list(map(text_node_to_html_node, child_node_list))

    def strip_lead_characters(text, block_type):
        if block_type is BlockType.ORDERED:
            regex = r"^[0-9]*\. "
            plain_text = re.split(regex, text)
            return plain_text[1]
        return text[2:]
    
    def text_to_code(text):
        split_list = text.split("\n")
        code_text = ""
        for line in split_list:
            if not line == "```":
                code_text += line + "\n"
        code = TextNode(code_text, TextType.CODE)
        return text_node_to_html_node(code)

    for block in block_list:
        block_type = block_to_block_type(block)
        lines = block.split("\n")
        match block_type:
            # Paragraphs
            case BlockType.PARAGRAPH:
                parent_node = ParentNode("p", text_to_child_node(block, block_type))
            # Heading
            case BlockType.HEADING:
                parent_node = decorate_header(block)
            # CodeBlock
            case BlockType.CODEBLOCK:
                parent_node = ParentNode("pre", [text_to_code(block)])
            # Quote Block
            case BlockType.QUOTE:
                new_lines = []
                for line in lines:
                    new_lines.append(strip_lead_characters(line, block_type))
                new_text = "\n".join(new_lines)
                parent_node = ParentNode("blockquote", text_to_child_node(new_text, block_type))
            # Unordered List
            case BlockType.UNORDERED:
                new_lines = []
                for line in lines:
                    new_lines.append("<li>" + strip_lead_characters(line, block_type) + "</li>")
                new_text = "\n".join(new_lines)
                parent_node = ParentNode("ul", text_to_child_node(new_text, block_type))
            # Ordered List
            case BlockType.ORDERED:
                new_lines = []
                for line in lines:
                    new_lines.append("<li>" + strip_lead_characters(line, block_type) + "</li>")
                new_text = "\n".join(new_lines)
                parent_node = ParentNode("ol", text_to_child_node(new_text, block_type))
        # Add all parents as children
        child_nodes.append(parent_node)
    html_node = ParentNode("div", child_nodes)
    return html_node
