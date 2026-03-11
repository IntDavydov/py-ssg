import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_tohtml(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        output = node.props_to_html()
        self.assertEqual(
            'href="https://www.google.com" target="_blank"'.strip(), output.strip()
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        output = node.props_to_html()
        self.assertEqual("", output)

    def test_repr(self):
        node = HTMLNode(
            "p", "what's up", [HTMLNode("span")], props={"tag": "no body cares"}
        )
        output = repr(node)
        self.assertIn(node.tag, output)
        self.assertIn(node.value, output)
        self.assertIn("span", output)
        self.assertIn("no body cares", output)


if __name__ == "__main__":
    unittest.main()
