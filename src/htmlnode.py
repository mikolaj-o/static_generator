import functools

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props else {}
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        dict_tuples = ""
        list_of_tuples = self.props.items()
        for att in list_of_tuples:
            dict_tuples += f' {att[0]}="{att[1]}"'
        return dict_tuples
    
    def __eq__(self, other):
        if isinstance(other, HTMLNode):
             if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
                 return True
        else:
            return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
        def __init__(self, tag=None, value=None, props=None):        
            self.props = props
            if value is None:
                raise ValueError("Need a value")
            super().__init__(tag=tag, value=value, props=props)

        def to_html(self):
            if self.value is None:
                raise ValueError("Need a value")
            if self.tag is None:
                return self.value
            else:
                if self.props == {}:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
                else:
                    property_ = self.props_to_html()
                    return f"<{self.tag}{property_}>{self.value}</{self.tag}>"
        
        def __eq__(self, other):
            if isinstance(other, LeafNode):
                if self.tag == other.tag and self.value == other.value and self.props == other.props:
                    return True
            else:
                return False
            
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        
        if tag is None:
            raise ValueError("Need a tag!")
        if not children:
            raise ValueError("Need a children!")
        super().__init__(tag=tag, children=children, props=props)
        self.children = children
        self.props = props if props else {}
        self.tag = tag
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Need a tag!")
        if not self.children:
            raise ValueError("Need a children!")
        HTMLstring = ""
        HTMLstring += f"<{self.tag}>"
        for child in self.children:
            HTMLstring += child.to_html()
        HTMLstring += f"</{self.tag}>"
        return HTMLstring

    def __eq__(self, other):
            if isinstance(other, ParentNode):
                if self.tag == other.tag and self.children == other.children and self.props == other.props:
                    return True
            else:
                return False

def text_node_to_html_node(text_node):
    types = ["text", "bold", "italic", "code", "link", "image"]
    if text_node.text_type not in types:
        raise Exception("Wrong text type")
    elif text_node.text_type == "text":
        return LeafNode(text=text_node.value)
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", text=text_node.value)
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", text=text_node.value)
    elif text_node.text_type == "link":
        return LeafNode(tag="a", text=text_node.value, props={"href": text_node.href})
    elif text_node.text_type == "image":
        return LeafNode(tag="img", value="", props={"src": text_node.src, "alt": text_node.alt})
    
    