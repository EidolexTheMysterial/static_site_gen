from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL_TYP = "normal"
    BOLD_TYP = "bold"
    ITALIC_TYP = "italic"
    CODE_TYP = "code"
    LINK_TYP = "link"
    IMG_TYP = "image"

# TextNode Class
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        ):
            return True

        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

# utilities
def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.NORMAL_TYP:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TYP:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TYP:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TYP:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TYP:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMG_TYP:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })

    raise ValueError(f"unhandled text type: {text_node.text_type}")
