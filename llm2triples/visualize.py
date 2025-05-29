from pyvis.network import Network

def visualize_knowledge_graph(graph, output_file="kg_graph.html"):
    """
    Visualizes a directed knowledge graph from a defaultdict where each key maps to a list of (object, predicate) tuples.

    Args:
        graph (dict): A dictionary where each key is a subject and maps to a list of (object, predicate) tuples.
        output_file (str): Path to the HTML file to save the graph visualization.

    Notes:
        - Nodes are added in lowercase to ensure uniqueness in display.
        - Predicates are shown as labels on the edges.
    """
    net = Network(height="750px", width="100%", directed=True, notebook=False)
    net.barnes_hut()
    added_nodes = set()

    for subj, triples in graph.items():
        subj_id = subj.lower()
        if subj_id not in added_nodes:
            net.add_node(subj_id, label=subj)
            added_nodes.add(subj_id)

        for obj, pred in triples:
            obj_id = obj.lower()
            if obj_id not in added_nodes:
                net.add_node(obj_id, label=obj)
                added_nodes.add(obj_id)

            net.add_edge(subj_id, obj_id, label=pred)

    if not net.nodes:
        raise ValueError("No nodes were added to the graph.")

    net.write_html(output_file)
    print(f"Graph saved to {output_file}. Open it in your browser.")
