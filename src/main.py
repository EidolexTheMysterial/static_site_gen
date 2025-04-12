from textnode import TextType, TextNode

from md_utils import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
)


def main():
    # new_tn = TextNode("my simple test", "link", "http://somesite.org")

    # print(new_tn)

    # txt_nd = TextNode("this is a **test**. end.", TextType.NORMAL_TYP)

    # new_nds = split_nodes_delimiter([ txt_nd ], "**", TextType.BOLD_TYP)

    # print(new_nds)

    # node = TextNode(
    #     "This is text with a [link](https://microsoft.com)[2nd link](https://mozilla.org). And more text.",
    #     TextType.NORMAL_TYP,
    # )

    node = TextNode("", TextType.NORMAL_TYP)

    new_nodes = split_nodes_link([node])

    print(new_nodes)

main()
