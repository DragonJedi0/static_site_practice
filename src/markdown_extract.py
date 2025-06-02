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
                    new_nodes.append(TextNode(text, TextType.TEXT))
                elif text:
                    new_nodes.append(TextNode(text, text_type))
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
        if node.text_type.value == "text":
            if not extract_markdown_images(node.text):
                new_nodes.append(node)
                continue
            else:
                current_text = node.text
                while(extract_markdown_images(current_text)):
                    image_alt, image_link = extract_markdown_images(current_text)[0]
                    text_before, text_after = current_text.split(f"![{image_alt}]({image_link})")
                    if text_before:
                        new_nodes.append(TextNode(text_before, TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                    if text_after and not extract_markdown_images(text_after):
                        new_nodes.append(TextNode(text_after, TextType.TEXT))
                    current_text = text_after
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value == "text":
            if not extract_markdown_links(node.text):
                new_nodes.append(node)
                continue
            else:
                current_text = node.text
                while(extract_markdown_links(current_text)):
                    link_text, link_url = extract_markdown_links(current_text)[0]
                    text_before, text_after = current_text.split(f"[{link_text}]({link_url})")
                    if text_before:
                        new_nodes.append(TextNode(text_before, TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                    if text_after and not extract_markdown_links(text_after):
                        new_nodes.append(TextNode(text_after, TextType.TEXT))
                    current_text = text_after
        else:
            new_nodes.append(node)
    return new_nodes
