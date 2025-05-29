from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must contain a tag")
        if self.children is None:
            raise ValueError("HTMLNode list cannot be None or empty")
        result = ""
        for child in self.children:
            result += child.to_html()       
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
