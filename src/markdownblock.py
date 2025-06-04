import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODEBLOCK = "code_block"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def block_to_block_type(markdown_block):
    if markdown_block:
        item_list = markdown_block.split("\n")
        for block_type in BlockType:
            item_check = []
            match block_type:
                case BlockType.HEADING:
                    # Heading
                    if re.findall(r"^(#){1,6} ", markdown_block):
                        return block_type
                case BlockType.CODEBLOCK:
                    # Code Block
                    if re.findall(r"^```[\s\S]*```$", markdown_block):
                        return block_type
                case BlockType.QUOTE:
                    # Quote
                    regex = r"^>"
                    if len(item_list) > 1:
                        for block in item_list:
                            if block:
                                if re.findall(regex, block):
                                    item_check.append(True)
                                else:
                                    item_check.append(False)
                        if not False in item_check:
                            return block_type
                    else:
                        if re.findall(regex, markdown_block):
                            return block_type
                case BlockType.UNORDERED:
                    # Unordered List
                    regex = r"^- "
                    if len(item_list) > 1:
                        for block in item_list:
                            if block:
                                if re.findall(regex, block):
                                    item_check.append(True)
                                else:
                                    item_check.append(False)
                        if not False in item_check:
                            return block_type
                    else:
                        if re.findall(regex, markdown_block):
                            return block_type
                case BlockType.ORDERED:
                    # Ordered
                    i = 1
                    regex = f"{i}\\. "
                    if len(item_list) > 1:
                        for block in item_list:
                            if block:
                                if re.findall(regex, block):
                                    item_check.append(True)
                                else:
                                    item_check.append(False)
                                i += 1
                                regex = f"{i}\\. "
                        if not False in item_check:
                            return block_type
                    else:
                        if re.findall(r"^1\. ", markdown_block):
                            return block_type

        return BlockType.PARAGRAPH
    else:
        raise Exception("Markdown block cannot be None or empty")
