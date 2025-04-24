import unittest

from md_utils import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html_node,
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


class TestMDToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    def test_headers(self):
        md = """
# this is an h1

## this is an h2

### this is an h3

####### this is not a header
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><h2>this is an h2</h2><h3>this is an h3</h3><p>####### this is not a header</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_blockquote(self):
        md = """
>this is some text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is some text</blockquote></div>",
        )

        md = """
a single para

>this is some text,
> and some more
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>a single para</p><blockquote>this is some text, and some more</blockquote></div>",
        )

        md = """
>line 1
>
>_line 3_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>line 1  <i>line 3</i></blockquote></div>",
        )


    def test_unord_list(self):
        md = """
- this is an item
- this is another item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is an item</li><li>this is another item</li></ul></div>",
        )

    def test_ord_list(self):
        md = """
1. this is an item
2. this is another item
3. and yet another item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is an item</li><li>this is another item</li><li>and yet another item</li></ol></div>",
        )

        md = """
1. this is an **item**
2. this is another item
3. and yet another item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is an <b>item</b></li><li>this is another item</li><li>and yet another item</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
