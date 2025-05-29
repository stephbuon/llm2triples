# llm2triples: Triples Extractor

Extracts (subject, predicate, object) triples from text using an LLM via `ask_groq`.

## Installation

```bash
pip install git+https://github.com/stephbuon/llm2triples.git
```

## Usage

Set groq API variable.

```python
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
```

Knowledge graphs from triples are created in two or optionally three steps. 

Step 1: `extract_triples()` 
Step 2: `build_knowledge_graph()`
- Purpose of fuzzy matching: When enabled, fuzzy matching helps resolve inconsistencies in node names. This attempts to treat semantically equivalent nodes as the same entity in the graph, rather than creating separate nodes for each variation. This is useful when:
    - Words are misspelled (e.g., "govenment" matched to "government")
    - Words are spelled differently but mean the same (e.g., "center" vs "centre")
Step 3: `dedeplicate_graph()`
- In case it is desirable to remove duplicate triples. 
Step 4: `visualize_knowledge_graph()`

```python
from llm2triples.extractor import extract_triples, build_knowledge_graph, deduplicate_graph
from llm2triples.prompts import extract_triples_prompt

# A list of sentences to analyze
sentences = [
    "He walked home.",
    "The dog jumped over the log.",
    "Maria gave her book to Elena."
]

# Extract triples
all_triples = []
for sentence in sentences:
    triples = extract_triples(sentence, extract_triples_prompt)
    all_triples.extend(triples)

# Build and deduplicate the knowledge graph
graph = build_knowledge_graph(all_triples, use_fuzzy_matching=True)
cleaned_graph = deduplicate_graph(graph)

# Print the result
for subject, edges in cleaned_graph.items():
    for obj, pred in edges:
        print(f"({subject}) -[{pred}]-> ({obj})")
```


```python
from llm2triples.visualize import visualize_knowledge_graph

# Assume `graph` is built and deduplicated
visualize_knowledge_graph(graph, output_file="my_graph.html")
```
