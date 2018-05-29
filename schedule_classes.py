import sys
import json
import pprint

class Node:
    def __init__(self, name, prereq_names):
        self.name = name
        self.prereq_names = prereq_names
        self.prereq_links = []
        self.tier = None


def parse_input(input_file):
    # read file
    entries = None
    try:
        file_handle = open(input_file, "r")
        file_content = file_handle.read()
        file_handle.close()
    except Exception as e:
        print e
        raise Exception ("Unable to read file")
    else:
        print file_content
        entries = json.loads(file_content)
    if not entries:
        raise Exception("No valid entries found in input file")
    return entries


def create_and_link_graph(entries):
    # create dict
    nodes = {}
    for entry in entries:
        nodes[entry['name']] = Node(entry['name'], entry['prerequisites'])

    # link prereqs
    for entry in nodes:
        node = nodes[entry]
        for prereq in node.prereq_names:
            if not prereq in nodes:
                raise Exception("Unable to find prequisite %s in input" % prereq)
            node.prereq_links.append(nodes[prereq])

    return nodes

def find_node_tier_if_ready(node):
    max_prereq_tier = -1 # 0 will be returned for nodes with no prereqs
    missing = None

    for prereq in node.prereq_links:
        if prereq.tier is None:
            # prereq node has not been processed yet
            missing = prereq
            break
        else:
            max_prereq_tier = max(max_prereq_tier, prereq.tier)

    return max_prereq_tier + 1, missing


def process_node(node, tiered_graph):
    print "Start Processing %s" % node.name

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
    print "Done Processing %s" % node.name


def organize_graph_by_tiers(nodes):
    tiered_graph = {}
    for node in nodes.values():
        if node.tier is None:
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
    nodes = create_and_link_graph(entries)

    # Organize graph by tiers (with DFS)
    print "\n--->Tiering the graph - to support BFS walking"
    tiered_graph = organize_graph_by_tiers(nodes)

    # BFS & output
    print "\n--->Producing Output by BFS walk"
    bfs_walk(tiered_graph)

    print "\n--->Done"

if __name__ == "__main__":
    main(sys.argv)
