from textnode import TextType, TextNode
from md_utils import split_nodes_delimiter

def main():
    new_tn = TextNode("my simple test", "link", "http://somesite.org")

    print(new_tn)

    txt_nd = TextNode("this is a **test**. end.", TextType.NORMAL_TYP)

    new_nds = split_nodes_delimiter([ txt_nd ], "**", TextType.BOLD_TYP)

    print(new_nds)

main()
