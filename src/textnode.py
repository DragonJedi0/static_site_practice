from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    text_type = TextType
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eg__(self, target):
        return (self.text == target.text and
                self.text_type == target.text_type and
                self.url == self.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
