import unittest

from textnode import TextNode, TextType
from converter import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodes(unittest.TestCase):
    def test_not_a_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "/", TextType.CODE)

    def test_type_code(self):
        node = TextNode("code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(node, new_nodes[0])

    def test_type_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_multibold(self):
        node = TextNode("This is text with a **bold** word **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_not_closed(self):
        node = TextNode("This is text with a **bold word **bold**", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_bold_italic(self):
        node = TextNode("This is text with a **bold** word _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.what.com) and another [second link](https://i.what.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.what.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.what.com"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        markdown_line = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(markdown_line)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes,
        )

    def test_markdown_to_blocks(self):
        markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """

        blocks = markdown_to_blocks(markdown)

        expected_list_block = (
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                expected_list_block,
            ],
            blocks,
        )

    def test_markdown_to_blocks_empty(self):
        markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.


        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """

        blocks = markdown_to_blocks(markdown)
        expected_list_block = (
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )

        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                expected_list_block,
            ],
            blocks,
        )

    def test_block_to_block_types(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.HEADING)

        block = "#This is a heading"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

        block = "```\nThis is a code\n```"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.CODE)

        block = "> This is a quote"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.QUOTE)

        block = "<This is a quote"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

        block = (
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

        block = (
            "-This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

        block = (
            "1. This is the first list item in a list block\n"
            "2. This is a list item\n"
            "3. This is another list item"
        )
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

        block = (
            "1This is the first list item in a list block\n"
            "2. This is a list item\n"
            "3. This is another list item"
        )
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.PARAGRAPH)
