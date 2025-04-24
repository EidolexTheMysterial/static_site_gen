import re
from enum import Enum

class BlockType(Enum):
    PARA_TYP = "paragraph"
    HEAD_TYP = "heading"
    CODE_TYP = "code"
    QUOTE_TYP = "quote"
    UNORD_TYP = "unordered list"
    ORD_TYP = "ordered list"

rxTtlHeader = r"^# (.+)$"

rxHeading = r"^#{,6} (.+)$"
rxCode = r"^```([\w\W]+)```$"
rxQuote = r"^>(.*)"
rxUnordered = r"^- (.+)"
rxOrdered = r"^\d+\. (.+)"


def block_to_block_type(block):
    if re.match(rxHeading, block):
        return BlockType.HEAD_TYP

    elif re.match(rxCode, block):
        return BlockType.CODE_TYP

    else:
        lines = block.split("\n")

        if all(map(lambda ln: re.match(rxQuote, ln), lines)):
            return BlockType.QUOTE_TYP

        elif all(map(lambda ln: re.match(rxUnordered, ln), lines)):
            return BlockType.UNORD_TYP

        elif all(map(lambda ln: re.match(rxOrdered, ln), lines)):
            return BlockType.ORD_TYP

        else:
            return BlockType.PARA_TYP


def get_block_val(block):
    typ = block_to_block_type(block)

    rx = None

    match typ:
        case BlockType.HEAD_TYP:
            rx = rxHeading

        case BlockType.CODE_TYP:
            rx = rxCode

        case BlockType.QUOTE_TYP:
            lines = block.split("\n")

            return " ".join(
                map(lambda ln: re.match(rxQuote, ln).group(1).strip(), lines)
            )

        case BlockType.UNORD_TYP:
            rx = rxUnordered

        case BlockType.ORD_TYP:
            rx = rxOrdered

        # PARA_TYP, all others
        case _:
            return block

    m = re.match(rx, block)

    return m.group(1).lstrip()


def extract_title(md):
    for ln in md.split("\n"):
        m = re.match(rxTtlHeader, ln)

        if m:
            return get_block_val(ln)

    raise Exception("Title header not fond")
