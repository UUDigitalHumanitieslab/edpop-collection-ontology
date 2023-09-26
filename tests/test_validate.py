from rdflib import Graph
from pathlib import Path
from rdflib.namespace import DCTERMS

ONTOLOGY_FILE = Path(__file__).parent.parent / 'ontology.ttl'
EXAMPLE_FILE =  Path(__file__).parent.parent / 'documentation' / 'example.ttl'

def test_valid_turtle():
    g = Graph()
    g.parse(ONTOLOGY_FILE)

    g.parse(EXAMPLE_FILE)

    assert g.triples((None, DCTERMS.creator, None))
