import unittest
#from colorama import Fore, Back, Style, init
#init(autoreset=True)
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextNode

class Test_HTML_Node(unittest.TestCase):
    #def setUp(self):
    #    print("\nStarting a new test...")
    #
    #def tearDown(self):
    #    print("Finished the test.")
    
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_no_props(self):
        node = HTMLNode(props={})
        #print("Testing node with no props...")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props(self):
        valid_value =  ' href="https://www.google.com" target="_blank"'
        prop = {
                    "href": "https://www.google.com", 
                    "target": "_blank",
                }
        node = HTMLNode(props=prop)
        #print(Fore.GREEN + f"\nRunning test on {prop}\nExpected: {valid_value}\nResult is {node.props_to_html()}\n")
        self.assertEqual(node.props_to_html(), valid_value)
    
    def test_single_prop(self):
        valid_value =  ' href="https://www.google.com"'
        prop = {
                    "href": "https://www.google.com", 
                }
        node = HTMLNode(props=prop)
        #print(Fore.BLUE + f"\nRunning test on {prop}\nExpected: {valid_value}\nResult is {node.props_to_html()}\n")
        self.assertEqual(node.props_to_html(), valid_value)        

    def test_proper_prop(self):
        valid_value =  '<a href="https://www.google.com">Click me!</a>'
        prop = {
                    "href": "https://www.google.com", 
                }
        tag1 = "a"
        value1 = "Click me!"
        node = LeafNode(tag=tag1, value=value1, props=prop)
        self.assertEqual(node.to_html(), valid_value)

    def test_proper_only_values(self):
        valid_value =  "A Value"
        #prop = {
        #            "href": "https://www.google.com", 
        #        }
        value1 = "A Value"
        node = LeafNode(value=value1)
        self.assertEqual(node.to_html(), valid_value)

    def test_proper_no_values(self):
        with self.assertRaises(ValueError):
            node = LeafNode()   

    def test_Parent(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                    None,
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )  

    def test_Parent_with_values(self):
        valid_value = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        node = ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
        self.assertEqual(node.to_html(), valid_value)
    

    


if __name__ == "__main__":
    unittest.main(verbosity=2)