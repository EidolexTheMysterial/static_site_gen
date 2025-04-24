import unittest

from blocktype import (
    BlockType,
    block_to_block_type,
    extract_title,
)


# Block Node tests
class BlockTypeTests(unittest.TestCase):
    def test_para_block(self):
        str = "test"

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.PARA_TYP)

    def test_head_block(self):
        str = "## test"

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.HEAD_TYP)

    def test_quote_block(self):
        str = """>this
>is a
>quote block"""

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.QUOTE_TYP)

        str += "\nline 4"

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.PARA_TYP)

    def test_unord_list(self):
        str = """- line 1
- line 2
- line 3"""

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.UNORD_TYP)

        str += "\nline 4"

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.PARA_TYP)

    def test_code_block(self):
        str = """```
some code
```
"""

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.CODE_TYP)

    def test_unord_list(self):
        str = """- line 1
- line 2
- line 3"""

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.UNORD_TYP)

        str += "\nline 4"

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.PARA_TYP)

    def test_ord_list(self):
        str = """1. line 1
2. line 2
3. line 3"""

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.ORD_TYP)

        str += "\nline 4"

        block_type = block_to_block_type(str)

        self.assertEqual(block_type, BlockType.PARA_TYP)

    def test_extract_title(self):
        md = """# My Title

## some other header
"""

        main_ttl = extract_title(md)

        self.assertEqual(main_ttl, "My Title")

        md = """

# This is the main header

rest of the markdown

"""

        main_ttl = extract_title(md)

        self.assertEqual(main_ttl, "This is the main header")


if __name__ == "__main__":
    unittest.main()
