import unittest

from md_utils import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
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

# Split Nodes tests
class TestSplitNodes(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TYP,
        )

        new_nodes = split_nodes_image([ node ])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TYP),
                TextNode("image", TextType.IMG_TYP, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TYP),
                TextNode(
                    "second image", TextType.IMG_TYP, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        # back-to-back images
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TYP,
        )

        new_nodes = split_nodes_image([ node ])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TYP),
                TextNode("image", TextType.IMG_TYP, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMG_TYP, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        # non-NORMAL-TYP test
        node = TextNode("bold", TextType.BOLD_TYP)

        new_nodes = split_nodes_image([ node ])

        self.assertListEqual([ TextNode("bold", TextType.BOLD_TYP) ], new_nodes)

        # empty text test
        node = TextNode("", TextType.NORMAL_TYP)

        new_nodes = split_nodes_image([ node ])

        self.assertListEqual([ TextNode("", TextType.NORMAL_TYP) ], new_nodes)


    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://microsoft.com) and another [2nd link](https://mozilla.org)",
            TextType.NORMAL_TYP,
        )

        new_nodes = split_nodes_link([ node ])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TYP),
                TextNode("link", TextType.LINK_TYP, "https://microsoft.com"),
                TextNode(" and another ", TextType.NORMAL_TYP),
                TextNode(
                    "2nd link", TextType.LINK_TYP, "https://mozilla.org"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with a [link](https://microsoft.com) and another [2nd link](https://mozilla.org). And more text.",
            TextType.NORMAL_TYP,
        )

        new_nodes = split_nodes_link([ node ])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TYP),
                TextNode("link", TextType.LINK_TYP, "https://microsoft.com"),
                TextNode(" and another ", TextType.NORMAL_TYP),
                TextNode(
                    "2nd link", TextType.LINK_TYP, "https://mozilla.org"
                ),
                TextNode(". And more text.", TextType.NORMAL_TYP),
            ],
            new_nodes,
        )

        # non-NORMAL-TYP test
        node = TextNode("bold", TextType.BOLD_TYP)

        new_nodes = split_nodes_link([ node ])

        self.assertListEqual([ TextNode("bold", TextType.BOLD_TYP) ], new_nodes)

        # empty text test
        node = TextNode("", TextType.NORMAL_TYP)

        new_nodes = split_nodes_link([ node ])

        self.assertListEqual([ TextNode("", TextType.NORMAL_TYP) ], new_nodes)


# Split Nodes tests
class TestTextToNodes(unittest.TestCase):
    def test_text_2nodes(self):
        txt = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(txt)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL_TYP),
                TextNode("text", TextType.BOLD_TYP),
                TextNode(" with an ", TextType.NORMAL_TYP),
                TextNode("italic", TextType.ITALIC_TYP),
                TextNode(" word and a ", TextType.NORMAL_TYP),
                TextNode("code block", TextType.CODE_TYP),
                TextNode(" and an ", TextType.NORMAL_TYP),
                TextNode("obi wan image", TextType.IMG_TYP, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL_TYP),
                TextNode("link", TextType.LINK_TYP, "https://boot.dev"),
            ],
            new_nodes,
        )


class TestMDBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
