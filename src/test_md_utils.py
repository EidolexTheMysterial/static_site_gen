import unittest

from md_utils import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, TextType

# Split Node tests
class TextNodeSplit(unittest.TestCase):
    def test_split(self):
            txt_nd = TextNode("this is a **test**. end.", TextType.NORMAL_TYP)

            new_nds = split_nodes_delimiter([ txt_nd ], "**", TextType.BOLD_TYP)

            self.assertEqual(len(new_nds), 3)

            txt_nd = TextNode("this **is** a **test**. end.", TextType.NORMAL_TYP)

            new_nds = split_nodes_delimiter([ txt_nd ], "**", TextType.BOLD_TYP)

            self.assertEqual(len(new_nds), 5)


# Extract Images tests
class TestExtractImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)


# Extract Links tests
class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://imgur.com/), and a [link2](http://another.com/)"
        )

        self.assertListEqual([
            ("link", "https://imgur.com/"),
            ("link2", "http://another.com/")
        ], matches)
