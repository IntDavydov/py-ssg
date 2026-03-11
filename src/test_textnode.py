import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_nourl(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_linktype(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.text_type, TextType.LINK)

    def test_imagetype(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertEqual(node.text_type, TextType.IMAGE)

    def test_italictype(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_codetype(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.text_type, TextType.CODE)

    def test_textype(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.text_type, TextType.TEXT)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
