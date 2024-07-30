import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_different_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic", "www.google.com")
        self.assertNotEqual(node, node2)

   

if __name__ == "__main__":
    unittest.main()