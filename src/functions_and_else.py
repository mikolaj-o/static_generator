
from textnode import (TextNode, text_type_code, text_type_bold, text_type_italic, text_type_text, text_type_link, text_type_image)
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    final_list_of_nodes = []
    
    
    for node in old_nodes:

            if node.text_type != text_type_text:
                final_list_of_nodes.append(node)
                continue
            
            
            node_to_list = node.text.split(delimiter)
            if len(node_to_list) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            for i in range(len(node_to_list)):
                if i % 2 == 0:
                    final_list_of_nodes.append(TextNode(node_to_list[i], text_type_text))
                else:
                    final_list_of_nodes.append(TextNode(node_to_list[i], text_type))
                            
    return final_list_of_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_link(old_nodes):
    total_nodes = []
    for node in old_nodes:
        if node.text =="":
            continue
        
        if node.text_type != text_type_text:
            total_nodes.append(node)
            continue
        node_tuples = extract_markdown_links(node.text)
        translator = lambda x: f"[{x[0]}]({x[1]})"
        result = []
        

        def splitter(text, dlmtrs):
            if dlmtrs == []:
                return [text]
            output_list_of_texts = []           
            delimiter = dlmtrs[0]
            part = text.split(delimiter)
            for d in part:
                output_list_of_texts += splitter(d, dlmtrs[1:])
            return output_list_of_texts
        
        delimiters = [translator(tup) for tup in node_tuples]
        only_text_list = splitter(node.text, delimiters)
        
        if delimiters == []:
            result.append(TextNode(node.text, text_type_text)) 
            total_nodes.extend(result)
        else:
            j = 0
            for i in range(len(only_text_list)):  
                if only_text_list[i] != "":
                    result.append(TextNode(only_text_list[i], text_type_text))
                if j < len(node_tuples):
                     result.append(TextNode(node_tuples[j][0], text_type_link, node_tuples[j][1]))
                     j += 1
            total_nodes.extend(result)
    return total_nodes

def split_nodes_image(old_nodes):
    total_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            total_nodes.append(node)
            continue
        if node.text =="":
            continue
        node_tuples = extract_markdown_images(node.text)
        translator = lambda x: f"[{x[0]}]({x[1]})"
        result = []

        def splitter(text, dlmtrs):
            if dlmtrs == []:
                return [text]
            output_list_of_texts = []           
            delimiter = dlmtrs[0]
            part = text.split(delimiter)
            if part[0].endswith('!'):
                part[0] = part[0].rstrip('!')

            for d in part:
                
                output_list_of_texts += splitter(d, dlmtrs[1:])
            return output_list_of_texts
        
        delimiters = [translator(tup) for tup in node_tuples]
        only_text_list = splitter(node.text, delimiters)
        
        if delimiters == []:
            result.append(TextNode(node.text, text_type_text)) 
            total_nodes.extend(result)
        else:
            j = 0
            for i in range(len(only_text_list)):  
                if only_text_list[i] != "":
                    result.append(TextNode(only_text_list[i], text_type_text))
                if j < len(node_tuples):
                     result.append(TextNode(node_tuples[j][0], text_type_image, node_tuples[j][1]))
                     j += 1
            total_nodes.extend(result)
    return total_nodes

def text_to_textnodes(text):
    dynamic_node = TextNode(text, text_type_text)
    return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([dynamic_node], "**", text_type_bold), "*", text_type_italic), "`", text_type_code)))
    

#test_text ="Here is some **bold text** mixed with *italic text* and `code snippets`. Now let's add an ![image](https://example.com/image.jpg) and [a link](https://example.com). How about combining **bold with `code`** and *italic with [a link](https://example.com)* together? And we should also see how it handles ![*italic image text*](https://example.com/italic-image.jpg) or ![**bold image text**](https://example.com/bold-image.png). Another line with ![image](https://different.com/image.jpg) and back to normal text."

test_text = "Here is some **bold text** in a sentence. Next, an *italic text* in another sentence. Followed by `inline code` in its sentence. Here is an ![example image](https://example.com/image.jpg). And finally, [a link](https://example.com) to round things off."

#for node in text_to_textnodes(test_text):
#    print(node)

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n")
    for block in block_list:
        if block == "":
            block_list.remove(block)

    j=0
    while j < len(block_list) - 1:
        
        if block_list[j].startswith("* ") and block_list[j + 1].startswith("* "):
            block_list[j] = f"{block_list[j]}\n{block_list[j + 1]}"
            block_list.pop(j + 1)
        else:
            j += 1
     
    block_list = [block.strip() for block in block_list]
    return block_list

markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\n Not a list item anymore."

print(markdown_to_blocks(markdown)[2])

def block_to_block_type(block):

    def num_list_check(text_block):
        checker = text_block.split(". ")
        if checker[0].isdigit():
            i = int(checker[0])
        else:
            return False
        
        result = []
        for line in text_block.split("\n"):
            if line.startswith(f"{i}. "):
                result.append(True)
                i += 1
            else:
                result.append(False)
                i +=1
        return all(result)
    
    if block.startswith("###### ") or block.startswith("##### ") or block.startswith("#### ") or block.startswith("### ") or block.startswith("## ") or block.startswith("# "):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in block.split("\n")):
        return "quote"
    elif all(block.startswith("* ") or block.startswith("- ") for line in block.split("\n")):
        return "unordered_list"
    elif num_list_check(block):
        return "ordered_list"
    else:
        return "paragraph"
    
complex_test_blocks = [
    "# Heading 1",                            # Heading
    "## Another heading\n### And another",    # Heading (First line being checked)
    "```\ndef foo():\n    return bar\n```",   # Code block
    "> Quote block start\n> Still quoting",   # Quote block
    "* Unordered item 1\n* Another item",     # Unordered list
    "- List item 1\n- List item 2",           # Unordered list
    "1. Ordered item 1\n2. Ordered item 2",   # Ordered list
    "10. Another ordered\n11. List item",     # Ordered list
    "Just a normal paragraph.",               # Paragraph
    "Paragraph with multiple\nlines in it.",  # Paragraph
    "#### A level 4 heading",                 # Heading
    "> Single line quote",                    # Quote block
    "```python\nprint('Code block')\n```",    # Code block with language hint
    "1. Mixed list\n2. With numbers\n- And a dash", # Shouldn't be matched strictly.
    "* Mixed list\n> With another type",      # Shouldn't be matched strictly.
    "> Nested quote\n> > Nested deeper",      # Quote block
]
test_blocks = [
                        "# Heading 1",                            # Heading
                        "## Heading 2",                           # Heading
                        "```\ncode block\n```",                   # Code block
                        "> Quote line 1\n> Quote line 2",         # Quote block
                        "* Unordered item 1\n* Unordered item 2", # Unordered list
                        "- Another unord item 1\n- Another 2",    # Unordered list
                        "1. Ordered item 1\n2. Ordered item 2",   # Ordered list
                        "Just a simple paragraph text.",          # Paragraph
                        "Normal text\nWith multiple lines.",      # Paragraph
                    ]

for b in complex_test_blocks:
    print(block_to_block_type(b))
    