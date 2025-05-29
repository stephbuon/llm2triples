from setuptools import setup, find_packages

setup(
    name='llm2triples',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'groq-client @ git+https://github.com/stephbuon/groq_client',
    ],
    author='Your Name',
    description='Extracts subject-predicate-object triples using an LLM',
)
