from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag, value):
        super().__init__(tag, value)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}>{self.value}</{self.tag}>"
