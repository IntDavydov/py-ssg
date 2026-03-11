import unittest

from converter import markdown_to_html_node


class TestMarkdownHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
            This is text that _should_ remain
            the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
            > This is quote
            > And this is what ?
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is quote And this is what ?</blockquote></div>",
        )

    def test_lists(self):
        md = """
            - This is an unordered item
            - This is another unordered item

            1. This is an ordered item
            2. This is another ordered item
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered item</li><li>This is another unordered item</li></ul><ol><li>This is an ordered item</li><li>This is another ordered item</li></ol></div>",
        )

    def test_heading(self):
        md = """
        # First heading
        ## Second heading
        ###### Sixs heading
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>First heading</h1><h2>Second heading</h2><h6>Sixs heading</h6></div>",
        )
