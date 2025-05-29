extract_triples_prompt = """
Return only the grammatical subject, verb, object and the object predicate 
triples stated in this sentence: {sentence}.
Return the triples like this: (text, text, text).

If there is a pronoun, put the referent of the pronoun after it like this <referent>. 

Here are some examples of what that should look like: 
(He <Max>, walked, home)
(Dog, jumped over, log)

Return an empty string if there are no triples.
"""
