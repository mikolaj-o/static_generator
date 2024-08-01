text_type_text="text"
text_type_code="code"
text_type_bold="bold"
text_type_italic="italic"
text_type_link="link"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if isinstance(other, TextNode):
             if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
                 return True
        else:
            return False
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
def main():
    print(TextNode("Dummy text", "bold", "www.google.com"))              


    
    