import unittest

from blocknode import BlockType, block_to_block_type

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


if __name__ == "__main__":
    unittest.main()
