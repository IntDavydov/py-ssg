import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node1 = LeafNode("b", "child")
        parent_node = ParentNode("div", [child_node, child_node1])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child</span><b>child</b></div>"
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])

        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()

        self.assertEqual(str(cm.exception), "Parent node must have a children")

    def test_to_html_nesting(self):
        child_node1 = LeafNode("b", "child")
        parent_node1 = ParentNode("p", [child_node1])

        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, parent_node1])

        self.assertEqual(
            parent_node.to_html(), "<div><span>child</span><p><b>child</b></p></div>"
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
