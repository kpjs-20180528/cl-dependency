import sys
import json
import pprint

class Node:
    def __init__(self, name, prereq_names):
        self.name = name
        self.prereq_names = prereq_names
        self.links = []
        self.tier = None


def parse_input(input_file):
    # read file
    f = open(input_file, "r")
    i = f.read()
    f.close()
    print i
    entries = json.loads(i)
    return entries


def create_nodes_dict(entries):
    nodes = {}
    for entry in entries:
        nodes[entry['name']] = Node(entry['name'], entry['prerequisites'])
    return nodes


def link_graph(nodes):
    for entry in nodes:
        node = nodes[entry]
        for prereq in node.prereq_names:
            node.links.append(nodes[prereq])


def find_node_tier_if_ready(node):
    max_prereq_tier = -1 # 0 will be returned for nodes with no prereqs
    missing = None

    for prereq in node.links:
        if prereq.tier is None:
            # prereq node has not been processed yet
            missing = prereq
            break
        else:
            max_prereq_tier = max(max_prereq_tier, prereq.tier)

    return max_prereq_tier + 1, missing


def process_node(node, tiered_graph):
    print "Processing %s" % node.name

    # find tier for node
    tier, missing = find_node_tier_if_ready(node)
    while (missing):
        # recursively find and set tier - DFS
        print "Missing %s while processing %s, recursing" % (missing.name, node.name)
        process_node(missing, tiered_graph)
        tier, missing = find_node_tier_if_ready(node)

    # set tier
    node.tier = tier

    # add to tiered graph
    if tier not in tiered_graph:
        tiered_graph[tier] = []
    tiered_graph[tier].append(node)


def organize_graph_by_tiers(nodes):
    tiered_graph = {}
    for node in nodes.values():
        process_node(node, tiered_graph)
    return tiered_graph


def bfs_walk(graph):
    print "Viable order"
    for tier in range(max(graph.keys())+1):
        print "Tier: %s" % tier
        for node in graph[tier]:
            print "\t%s" % node.name


def main(args):
    # Process Input
    print "--->Processing Input File %s" % args[1]
    entries = parse_input(args[1])

    # create and Link the nodes
    print "\n--->Building the graph"
    nodes = create_nodes_dict(entries)
    link_graph(nodes)

    # Organize graph by tiers (with DFS)
    print "\n--->Tiering the graph - to support BFS walking"
    tiered_graph = organize_graph_by_tiers(nodes)

    # BFS & output
    print "\n--->Producing Output by BFS walk"
    bfs_walk(tiered_graph)

    print "\n--->Done"

if __name__ == "__main__":
    main(sys.argv)
