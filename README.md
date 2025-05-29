# Triple Extractor

Extracts (subject, predicate, object) triples from text using an LLM via `ask_groq`.

## Installation

```bash
pip install -e .
```

## Usage

```python
from triple_extractor.extractor import extract_triples, build_knowledge_graph, deduplicate_graph
from triple_extractor.prompts import extract_triples_prompt

sentences = ["He walked home.", "The dog jumped over the log."]
all_triples = []

for s in sentences:
    all_triples.extend(extract_triples(s, extract_triples_prompt))

graph = build_knowledge_graph(all_triples, use_fuzzy_matching=True)
graph = deduplicate_graph(graph)
```
