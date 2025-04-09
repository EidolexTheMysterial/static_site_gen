import unittest

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HtmlNode, LeafNode, ParentNode

# HTMLNode tests
class TestHtmlNode(unittest.TestCase):
    def test_props(self):
        node = HtmlNode("h1", "test val", props={ "color": "blue" })
        props_html = node.props_to_html()

        self.assertEqual(props_html, ' color="blue"')

        node2 = HtmlNode("h1", "test val", props={ "color": "blue", "font": "Arial" })
        props_html2 = node2.props_to_html()

        self.assertEqual(props_html2, ' color="blue" font="Arial"')

    def test_no_props(self):
        node = HtmlNode("h1")
        props_html = node.props_to_html()
        self.assertEqual(props_html, "")


# LeafNode tests
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Test Link", { "href": "http://test.org" })
        self.assertEqual(node2.to_html(), '<a href="http://test.org">Test Link</a>')


# ParentNode tests
class TestParentNode(unittest.TestCase):
    def test_parent_to_html_nochild(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

        node2 = ParentNode("p", [], { "color": "blue" })
        self.assertEqual(node2.to_html(), '<p color="blue"></p>')

    def test_parent_to_html(self):
        ch_node1 = LeafNode("b", "My Header")
        node = ParentNode("p", [ ch_node1 ])

        self.assertEqual(node.to_html(), "<p><b>My Header</b></p>")

        node2 = ParentNode("p", [ ch_node1 ], { "color": "red" })

        self.assertEqual(node2.to_html(), '<p color="red"><b>My Header</b></p>')

    # from Boot.dev lesson
    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children2(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


# Conversion tests
class TestNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TYP)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a test link", TextType.LINK_TYP, "https://microsoft.com")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a test link")

        self.assertEqual(html_node.to_html(), '<a href="https://microsoft.com">This is a test link</a>')


if __name__ == "__main__":
    unittest.main()
