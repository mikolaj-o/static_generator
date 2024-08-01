
from textnode import (TextNode, text_type_code, text_type_bold, text_type_italic, text_type_text, text_type_link)
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    final_list_of_nodes = []
    
    
    for node in old_nodes:
            if node.text_type != text_type_text:
                list_of_nodes.append(node)
            if delimiter == "**":
                text_case = text_type_bold
            elif delimiter == "`":
                text_case = text_type_code
            elif delimiter == "*" and "**" not in node.text:
                text_case = text_type_italic
            else:
                final_list_of_nodes.append(node)
                continue
            
            node_to_list = node.text.split(delimiter)
            if len(node_to_list) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            for i in range(len(node_to_list)):
                if i % 2 == 0:
                    final_list_of_nodes.append(TextNode(node_to_list[i], text_type_text))
                else:
                    final_list_of_nodes.append(TextNode(node_to_list[i], text_case))
                            
    return final_list_of_nodes
    
node1 = TextNode("Pudle są bardzo *inteligentnymi* psami, które często występują na wystawach. Ich futro jest *kręcone, gęste* i wymaga pielęgnacji.", "text")
node2 = TextNode("Pudle posiadają zwinne ciała, dzięki **którym** potrafią wykonywać trudne sztuczki. Są również **przyjazne** i łatwe do tresury.", "text")
node3 = TextNode("Pudle są bardzo `inteligentnymi` psami, które często występują na wystawach. Ich futro jest `kręcone, gęste` i wymaga pielęgnacji.", "text")


node_to_change = [node1, node2, node3]

new_nodes = split_nodes_delimiter(node_to_change, "**", "bold")


def extract_markdown_images(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_link(old_nodes):
    total_nodes = []
    for node in old_nodes:
        if node.text =="":
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
            for i in range(len(only_text_list)+len(delimiters)-2):  
                if only_text_list[i] != "":
                    result.append(TextNode(only_text_list[i], text_type_text))
                if i >= len(delimiters):
                    break 
                result.append(TextNode(node_tuples[i][0], text_type_link, node_tuples[i][1]))
            total_nodes.extend(result)
    return total_nodes

node = TextNode(
    "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
    text_type_text,
)

node2 = TextNode(
    "------ONLY TEXT-------",
    text_type_text,
)

node3 = TextNode(
    "",
    text_type_text,
)

node4 = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
    text_type_text,
)

new_nodes = split_nodes_link([node, node2, node3, node4])
for node in new_nodes:
    print(node)
