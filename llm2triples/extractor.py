import re
import csv
from collections import defaultdict
from difflib import SequenceMatcher
from groq_client import ask_groq

def extract_triples(sentence, prompt_template):
    prompt = prompt_template.format(sentence=sentence)
    groq_output = ask_groq(prompt)
    triple_pattern = re.findall(r'\(([^)]+)\)', groq_output)

    triples = []
    for triple in triple_pattern:
        parts = [part.strip() for part in triple.split(',')]
        if len(parts) == 3:
            triples.append(tuple(parts))
    return triples

def match_node_name(name, existing_nodes, threshold=0.8, fuzzy_writer=None):
    for node in existing_nodes:
        ratio = SequenceMatcher(None, name.lower(), node.lower()).ratio()
        if ratio > threshold:
            if fuzzy_writer:
                fuzzy_writer.writerow({
                    "original": name,
                    "matched": node,
                    "similarity": round(ratio, 3)
                })
            return node
    return name

def build_knowledge_graph(triples, use_fuzzy_matching=True, log_file="fuzzy_matches.csv"):
    graph = defaultdict(list)
    all_nodes = set()
    fuzzy_writer = None

    if use_fuzzy_matching:
        fuzzy_log_file = open(log_file, "w", newline="", encoding="utf-8")
        fuzzy_writer = csv.DictWriter(fuzzy_log_file, fieldnames=["original", "matched", "similarity"])
        fuzzy_writer.writeheader()

    for subj, pred, obj in triples:
        if use_fuzzy_matching:
            subj = match_node_name(subj, all_nodes, fuzzy_writer=fuzzy_writer)
            obj = match_node_name(obj, all_nodes, fuzzy_writer=fuzzy_writer)

        graph[subj].append((obj, pred))
        all_nodes.update([subj, obj])

    if fuzzy_writer:
        fuzzy_log_file.close()

    return graph

def deduplicate_graph(graph):
    cleaned_graph = defaultdict(list)
    for subj, edges in graph.items():
        seen = set()
        for obj, pred in edges:
            if (obj, pred) not in seen:
                cleaned_graph[subj].append((obj, pred))
                seen.add((obj, pred))
    return cleaned_graph
