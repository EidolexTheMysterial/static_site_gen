import re
from textnode import TextType, TextNode

rxMdImages = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
rxMdLinks = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

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
    current_lst = split_nodes_image([ TextNode(text, TextType.NORMAL_TYP) ])

    current_lst = split_nodes_link(current_lst)

    current_lst = split_nodes_delimiter(current_lst, "**", TextType.BOLD_TYP)
    current_lst = split_nodes_delimiter(current_lst, "_", TextType.ITALIC_TYP)
    current_lst = split_nodes_delimiter(current_lst, "`", TextType.CODE_TYP)

    return current_lst

# split md into list of non-empty blocks
def markdown_to_blocks(markdown):
    new_lst = []

    txt_blocks = markdown.split("\n\n")

    for b in txt_blocks:
        b = b.strip()

        if len(b) > 0:
            new_lst.append(b)

    return new_lst
