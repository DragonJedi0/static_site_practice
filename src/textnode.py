from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    text_type = TextType
    def __init__(self, text, text_type, url=None):
        if text_type in TextType:
            self.text = text
            self.text_type = text_type
            self.url = url
        else:
            raise Exception("Invalid Text Type")

    def __eq__(self, target):
        return (self.text == target.text and
                self.text_type == target.text_type and
                self.url == target.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
