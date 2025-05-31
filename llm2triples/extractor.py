import os
import re
import csv
from collections import defaultdict
from difflib import SequenceMatcher
from groq_client import ask_groq

import re
from groq_client import ask_groq

def contains_pronoun(sentence):
    PRONOUNS = {"he", "she", "they", "it", "his", "her", "their", "him", "them"}
    words = re.findall(r'\b\w+\b', sentence.lower())
    return any(word in PRONOUNS for word in words)

#def resolve_pronouns(chunk, sentences, prompt_template, n=10, model='llama3-8b-8192'):
#    resolutions = []
#    for i, sentence in enumerate(sentences):
#        if contains_pronoun(sentence):
#            context = sentences[max(0, i-n):i]  # By default, get up to 10 previous sentences as context to resolve pronouns
#            context_text = " ".join(context)
#
#            prompt = prompt_template.format(context_text=context_text, sentence=sentence)
#            response = ask_groq(prompt, model)
#
#            resolutions.append(response)
#        else:
#            resolutions.append(sentence)
#    return resolutions

def resolve_pronouns(chunk, sentences, prompt_template, n=10, model='llama3-8b-8192'):
    resolutions = []
    for sentence in sentences:
        try:
            idx = chunk.index(sentence)  # Find the index of this sentence in the chunk
        except ValueError:
            resolutions.append(sentence)
            continue

        if contains_pronoun(sentence):
            context = chunk[max(0, idx - n):idx]
            context_text = " ".join(context)

            prompt = prompt_template.format(context_text=context_text, sentence=sentence)
            response = ask_groq(prompt, model=model)

            resolutions.append(response)
        else:
            resolutions.append(sentence)
    return resolutions

def extract_triples(sentence, prompt_template, model="llama-3.3-70b-versatile"):
    prompt = prompt_template.format(sentence=sentence)
    groq_output = ask_groq(prompt, model)
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
        log_exists = os.path.isfile(log_file)
        fuzzy_log_file = open(log_file, "a", newline="", encoding="utf-8")
        fuzzy_writer = csv.DictWriter(fuzzy_log_file, fieldnames=["original", "matched", "similarity"])
        if not log_exists:
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
