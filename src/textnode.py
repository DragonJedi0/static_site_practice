from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    text_type = TextType
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        return (self.text == target.text and
                self.text_type == target.text_type and
                self.url == target.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception("Cannot Convert: Not a valid TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:

        # Verify node is not Text type
        if not node.text_type.value == "text":

            try:
                # Split the node text into list of strings
                node_text = node.text.split(delimiter)
                if len(node_text) == 2:
                    raise Exception("No closing delimiter found. Delimiter must surround target text")

                # Go through each element, assigning every other element as text_type
                plain_text = True
                for text in node_text:
                    if plain_text:
                        new_nodes.extend(TextNode(text, TextType.TEXT, node.url))
                    else:
                        new_nodes.extend(TextNode(text, text_type, node.url))
                    # Flip boolean
                    plain_text = not plain_text
                
            except Exception as e:
                raise e

        else:
            new_nodes.extend(node)
    
    return new_nodes
