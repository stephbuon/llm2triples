# Triples Extractor

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

Knowledge graphs from triples are c

`extract_triples()`: 

`build_knowledge_graph()`

`dedeplicate_graph()`:


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
