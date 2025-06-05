import re
from enum import Enum

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
