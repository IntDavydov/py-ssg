import unittest

from generate_page import extract_title


class TestSplitNodes(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
        # Some title
        """

        title = extract_title(markdown)
        self.assertEqual("Some title", title)

        markdown = """
        - there should be
        - the title 

        1. even if it's on the bottom

        # Some title
        """

        title = extract_title(markdown)
        self.assertEqual("Some title", title)

        markdown = """
        #Some title
        """

        with self.assertRaises(ValueError):
            extract_title(markdown)
