import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYP)
        node2 = TextNode("This is a text node", TextType.BOLD_TYP)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYP, "http://test.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TYP, "http://test.com")
        self.assertEqual(node, node2)

    def test_txt_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYP)
        node2 = TextNode("This is a text node!", TextType.BOLD_TYP)
        self.assertNotEqual(node, node2)

    def test_typ_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYP)
        node2 = TextNode("This is a text node", TextType.ITALIC_TYP)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYP, "http://test.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TYP, "http://testing.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
