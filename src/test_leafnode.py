import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "whaare u ding hiere")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "whaare u ding hiere")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_tohtml_novalue(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tohtml_notag(self):
        node = LeafNode("", "whaare u ding hiere")
        output = node.to_html()
        self.assertEqual(output, "whaare u ding hiere")

    def test_tohtml(self):
        node = LeafNode("p", "whaare u ding hiere")
        output = node.to_html()
        self.assertEqual(
            output, f"<{node.tag}{node.props_to_html()}>{node.value}</{node.tag}>"
        )

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("p", "whaare u ding hiere", props=props)
        output = node.props_to_html()
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"'.strip(), output.strip()
        )

    def test_props_to_html_empty(self):
        node = LeafNode("p", "whaare u ding hiere")
        output = node.props_to_html()
        self.assertEqual("", output)

    def test_repr(self):
        node = LeafNode("p", "what's up", props={"tag": "no body cares"})
        output = repr(node)
        self.assertIn(node.tag, output)
        self.assertIn(node.value, output)
        self.assertIn("no body cares", output)
