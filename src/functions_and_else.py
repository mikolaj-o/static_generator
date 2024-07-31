
from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_case = ""
    list_of_nodes = []
    final_list_of_nodes = []
    
    
    for node in old_nodes:
            if node.text_type != "text":
                list_of_nodes.append(node)
            
            if delimiter == "**":
                text_case = "bold"
            elif delimiter == "'":
                text_case = "code"
            elif delimiter == "*" and "**" not in node.text:
                text_case = "italic"
            else:
                list_of_nodes.append(node)
                continue
            
            node_to_list = node.text.split(delimiter)
            i = 0
            while i < len(node_to_list):
                list_of_nodes.append(TextNode(node_to_list[0 + i], None))
                if i == len(node_to_list) - 1 :
                    break
                list_of_nodes.append(TextNode(node_to_list[1 + i], text_case))
                i += 2
                
            final_list_of_nodes.extend(list_of_nodes)
            
    return final_list_of_nodes
    
node1 = TextNode("Pudle są bardzo *inteligentnymi* psami, które często występują na wystawach. Ich futro jest *kręcone, gęste* i wymaga pielęgnacji.", "text")
node2 = TextNode("Pudle posiadają zwinne ciała, dzięki **którym** potrafią wykonywać trudne sztuczki. Są również **przyjazne** i łatwe do tresury.", "text")
node3 = TextNode("Pudle są bardzo *inteligentnymi* psami, które często występują na wystawach. Ich futro jest *kręcone, gęste* i wymaga pielęgnacji.", "text")


node_to_change = [node1, node2, node3]

new_nodes = split_nodes_delimiter(node_to_change, "*", "italic")

for item in new_nodes:

    print(f"{item}")