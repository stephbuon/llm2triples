# Will not work well if given a sentence with all pronouns and no referent. 
extract_triples_and_resolve_pronouns_prompt = """
Return only the grammatical subject, verb, object and the object predicate 
triples stated in this sentence: {sentence}.
Return the triples like this: (text, text, text).

If there is a pronoun, put the referent of the pronoun after it like this <referent>. 

Here are some examples of what that should look like: 
(He <Max>, walked, home)
(Dog, jumped over, log)

Return an empty string if there are no triples.
"""

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

# First programmatically check if there is a pronoun. 
resolve_pronouns_prompt = """
Resolve pronouns in this text by putting the referent of the pronoun after it, like this: <referent>. 

Max rode his <Max's> bike home on Sunday. 
After Maria gave the book to Anna, she <Maria> told her <Anna> that she <Anna> needed to return it by Friday because the librarian said it was overdue.

Return just the sentence and no other text. 
"""
