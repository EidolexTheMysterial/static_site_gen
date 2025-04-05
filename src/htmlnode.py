# HtmlNode Class
class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_txt(self, pfix, sep):
        return pfix + sep.join(
            map(lambda attr: f'{attr}="{self.props[attr]}"', self.props)
            )

    def to_html(self):
        raise NotImplementedError("tbd")

    def props_to_html(self):
        if self.props:
            return self.props_to_txt(" ", " ")
        return ""

    def __repr__(self):
        out = f"HtmlNode(Tag={self.tag}, Value={self.value})"

        if self.props != None:
            out += self.props_to_txt("\n\nProps:\n  ", "\n  ")

        if self.children != None:
            out += "\n\nChildren:\n"
            out += "-" * 40 + "\n"
            out += "\n".join(map(lambda child: str(child), self.children)) + "\n"
            out += "-" * 40 + "\n"

        return out

# LeafNode Class
class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

# ParentNode Class
class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")

        child_html = "".join(map(lambda child: child.to_html(), self.children))

        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
