import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    match (delimiter, text_type):
        case ("**", TextType.BOLD):
            match = True
        case ("_", TextType.ITALIC):
            match = True
        case ("`", TextType.CODE):
            match = True

        case _:
            match = False

    if not match:
        raise TypeError("Delimiter does not match with TextType")

    new_nodes = []
    for node in old_nodes:
        # Verify node is not Text type
        if node.text_type.value == "text":
            # Split the node text into list of strings
            node_text = node.text.split(delimiter)
            if len(node_text) % 2 == 0:
                raise Exception("No closing delimiter found. Delimiter must surround target text")
            # Go through each element, assigning every other element as text_type
            plain_text = True
            for text in node_text:
                if plain_text and text:
                    new_nodes.append(TextNode(text, TextType.TEXT, node.url))
                elif text:
                    new_nodes.append(TextNode(text, text_type, node.url))
                # Flip boolean
                plain_text = not plain_text
        else:
            new_nodes.append(node)
    
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "text":
            node_text = node.text.split()
            plain_text = True
            for text in node_text:
                if plain_text and text:
                    new_nodes.append(TextNode(text, TextType.TEXT, node.url))
                elif text:
                    new_nodes.append(TextNode(text), TextType.IMAGE, node.url)
                plain_text = not plain_text
        else:
            new_nodes.append(node)
    return new_nodes
