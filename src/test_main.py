import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello There\n\n## The many phrases of Obi-wan Kenobi"
        header = extract_title(markdown)
        self.assertEqual(header.to_html(), "<h1>Hello There</h1>")

    def test_no_title(self):
        markdown = "## This is the wrong level Header\n\nYou! Shall not! Pass!"
        with self.assertRaises(Exception) as e:
            extract_title(markdown)
        err_msg = e.exception
        self.assertEqual(str(err_msg), "No Title found in markdown provided")
