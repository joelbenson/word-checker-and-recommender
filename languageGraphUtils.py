import networkx as nx
import json
import time

#Save language graph to path with .lg file extension
def save_lg(G, path):

    with open(path, 'w+') as file:

        for node in G.nodes:
            node_info = {}
            node_info["type"] = "node"
            node_info["label"] = node
            node_info["attributes"] = G.node[node]
            file.write(json.dumps(node_info)+"\n")

        for edge in G.edges:
            data = G.get_edge_data(edge[0], edge[1])

            edge_info = {}
            edge_info["type"] = "edge"
            edge_info["nodes"] = (edge[0],edge[1])
            edge_info["key"] = list(data.keys())[0]
            edge_info["attributes"] = list(data.values())[0]
            file.write(json.dumps(edge_info)+"\n")

    return


def read_lg(path):

    G = nx.MultiGraph()

    with open(path, 'r') as file:
        for line in file:

            object = json.loads(line)

            if (object["type"] == "node"):
                label = object["label"]
                attributes = object["attributes"]

                G.add_node(label, attr_dict=attributes)

            elif(object["type"] == "edge"):
                nodes = object["nodes"]
                key = object["key"]

                if (key == "co-occurance"):
                    attributes = object["attributes"]
                    G.add_edge(nodes[0], nodes[1], key=key, count=attributes["count"])

                elif (key == "synonym"):
                    G.add_edge(nodes[0], nodes[1], key=key)

    return G
