import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_lst = []

    for nd in old_nodes:
        if nd.text_type != TextType.NORMAL_TYP:
            new_lst.append(nd)
            continue

        blocks = nd.text.split(delimiter)

        if len(blocks) % 2 == 0:
            raise ValueError("invalid markdown syntax")

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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches
