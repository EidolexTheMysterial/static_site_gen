import sys

from file_ops import (
    start_file_ops,
    start_gen_ops,
)


def main():
    print(f"\n**[ starting static_site_gen ]**\n")

    base_path = "/"

    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    start_file_ops()

    start_gen_ops(base_path)



    # new_tn = TextNode("my simple test", "link", "http://somesite.org")

    # print(new_tn)

    # txt_nd = TextNode("this is a **test**. end.", TextType.NORMAL_TYP)

    # new_nds = split_nodes_delimiter([ txt_nd ], "**", TextType.BOLD_TYP)

    # print(new_nds)

    # node = TextNode(
    #     "This is text with a [link](https://microsoft.com)[2nd link](https://mozilla.org). And more text.",
    #     TextType.NORMAL_TYP,
    # )

    # node = TextNode("", TextType.NORMAL_TYP)

    # new_nodes = split_nodes_link([node])

    # print(new_nodes)

main()
