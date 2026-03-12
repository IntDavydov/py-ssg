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
            - This is another unordered item with **bold** text

            1. This is an ordered item
            2. This is another ordered item with _italic_ text
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered item</li><li>This is another unordered item with <b>bold</b> text</li></ul><ol><li>This is an ordered item</li><li>This is another ordered item with <i>italic</i> text</li></ol></div>",
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

    def test_links(self):
        md = """
        ![JRR Tolkien sitting](/images/tolkien.png)
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><img src="/images/tolkien.png" alt="JRR Tolkien sitting"></img></p></div>',
        )

        md = """
             - [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li></ul></div>',
        )

        md = """
            Want to get in touch? [Contact me here](/contact).
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Want to get in touch? <a href="/contact">Contact me here</a>.</p></div>',
        )

        md = """
            This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This site was generated with a custom-built <a href="https://www.boot.dev/courses/build-static-site-generator-python">static site generator</a> from the course on <a href="https://www.boot.dev">Boot.dev</a>.</p></div>',
        )
