import re

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HtmlNode, LeafNode, ParentNode
from blocktype import BlockType, block_to_block_type, get_block_val

rxMdImages = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
rxMdLinks = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

rxHeadStart = r"^#{,6}"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_lst = []

    for nd in old_nodes:
        if nd.text_type != TextType.NORMAL_TYP:
            new_lst.append(nd)
            continue

        blocks = nd.text.split(delimiter)

        if len(blocks) % 2 == 0:
            raise ValueError(f"invalid markdown syntax; delimiter {delimiter}")

        split_nds = []

        for i in range(len(blocks)):
            if len(blocks[i]) == 0:
                continue
            if i % 2 == 0:
                split_nds.append(TextNode(blocks[i], TextType.NORMAL_TYP))
            else:
                split_nds.append(TextNode(blocks[i], text_type))

        new_lst.extend(split_nds)

    return new_lst

# Split utils

def extract_markdown_images(text):
    matches = re.findall(rxMdImages, text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(rxMdLinks, text)

    return matches

def handle_split_nodes(current_txt, split_nds, is_image):
    nd_lst = []

    prefix = ""
    typ = TextType.LINK_TYP

    if is_image:
        prefix = "!"
        typ = TextType.IMG_TYP

    next_block = current_txt

    for txt, url in split_nds:
        blocks = next_block.split(f"{prefix}[{txt}]({url})", 1)

        if len(blocks) != 2:
            raise ValueError(f"invalid markdown syntax, {typ.value} is not closed")

        if len(blocks[0]) > 0:
            nd_lst.append(TextNode(blocks[0], TextType.NORMAL_TYP))

        nd_lst.append(TextNode(txt, typ, url))

        next_block = blocks[1]

    if len(next_block) > 0:
        nd_lst.append(TextNode(next_block, TextType.NORMAL_TYP))

    return nd_lst


def split_nodes_image(old_nodes):
    new_lst = []

    for nd in old_nodes:
        if nd.text_type != TextType.NORMAL_TYP:
            new_lst.append(nd)
            continue

        img_nds = extract_markdown_images(nd.text)

        if len(img_nds) == 0:
            new_lst.append(nd)
            continue

        # get images
        new_lst.extend(handle_split_nodes(nd.text, img_nds, True))

    return new_lst

def split_nodes_link(old_nodes):
    new_lst = []

    for nd in old_nodes:
        if nd.text_type != TextType.NORMAL_TYP:
            new_lst.append(nd)
            continue

        lnk_nds = extract_markdown_links(nd.text)

        if len(lnk_nds) == 0:
            new_lst.append(nd)
            continue

        # get links
        new_lst.extend(handle_split_nodes(nd.text, lnk_nds, False))

    return new_lst

# text to text_nodes
def text_to_textnodes(text):
    nd_lst = split_nodes_image([ TextNode(text, TextType.NORMAL_TYP) ])

    nd_lst = split_nodes_link(nd_lst)

    nd_lst = split_nodes_delimiter(nd_lst, "**", TextType.BOLD_TYP)
    nd_lst = split_nodes_delimiter(nd_lst, "_", TextType.ITALIC_TYP)
    nd_lst = split_nodes_delimiter(nd_lst, "`", TextType.CODE_TYP)

    return nd_lst

# split md into list of non-empty blocks
def markdown_to_blocks(markdown):
    new_lst = []

    blocks = markdown.split("\n\n")

    for b in blocks:
        b = b.strip()

        if len(b) > 0:
            new_lst.append(b)

    return new_lst


# Conversion helpers

# return "h[1-6]" based on the number of #s at the start
def get_header_tag(str):
    m = re.match(rxHeadStart, str)

    return f"h{len(m[0])}"


def handle_list_typ(typ, block):
    tag = "ul" if typ == BlockType.UNORD_TYP else "ol"

    inline_nds = []

    for ln in block.split("\n"):
        val = get_block_val(ln)

        nd_lst = text_to_children(val)

        inline_nds.append(ParentNode("li", nd_lst))

    return ParentNode(tag, inline_nds)


def text_to_children(text):
    text = text.replace("\n", " ")

    txt_nds = text_to_textnodes(text)

    html_nds = list(map(lambda nd: text_node_to_html_node(nd), txt_nds))

    return html_nds


def markdown_to_html_node(markdown):
    nd_lst = []
    blocks = markdown_to_blocks(markdown)

    for b in blocks:
        child_nd = None

        match block_to_block_type(b):
            case BlockType.HEAD_TYP:
                tag = get_header_tag(b)
                val = get_block_val(b)

                child_nd = ParentNode(tag, text_to_children(val))

            case BlockType.CODE_TYP:
                val = get_block_val(b)

                nd = TextNode(val, TextType.CODE_TYP)

                child_nd = ParentNode("pre", [ text_node_to_html_node(nd) ])

            case BlockType.QUOTE_TYP:
                val = get_block_val(b)

                child_nd = ParentNode("blockquote", text_to_children(val))

            case BlockType.PARA_TYP:
                val = get_block_val(b)

                child_nd = ParentNode("p", text_to_children(val))

            case BlockType.UNORD_TYP:
                child_nd = handle_list_typ(BlockType.UNORD_TYP, b)

            case BlockType.ORD_TYP:
                child_nd = handle_list_typ(BlockType.ORD_TYP, b)

        nd_lst.append(child_nd)

    return ParentNode("div", nd_lst)
