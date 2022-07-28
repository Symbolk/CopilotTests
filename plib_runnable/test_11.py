"""
Some utility functions.

Miscellaneous utilities

* list2set
* first
* uniq
* more_than

Term characterisation and generation

* to_term
* from_n3

Date/time utilities

* date_time
* parse_date_time

"""

from calendar import timegm
from os.path import splitext

# from time import daylight
from time import altzone, gmtime, localtime, time, timezone
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
)

import rdflib.graph  # avoid circular dependency
from rdflib.compat import sign
from rdflib.namespace import XSD, Namespace, NamespaceManager
from rdflib.term import BNode, IdentifiedNode, Literal, Node, URIRef

if TYPE_CHECKING:
    from rdflib.graph import Graph

__all__ = [
    "list2set",
    "first",
    "uniq",
    "more_than",
    "to_term",
    "from_n3",
    "date_time",
    "parse_date_time",
    "guess_format",
    "find_roots",
    "get_tree",
    "_coalesce",
]



SUFFIX_FORMAT_MAP = {
    "xml": "xml",
    "rdf": "xml",
    "owl": "xml",
    "n3": "n3",
    "ttl": "turtle",
    "nt": "nt",
    "trix": "trix",
    "xhtml": "rdfa",
    "html": "rdfa",
    "svg": "rdfa",
    "nq": "nquads",
    "nquads": "nquads",
    "trig": "trig",
    "json": "json-ld",
    "jsonld": "json-ld",
    "json-ld": "json-ld",
}


def find_roots(
    graph: "Graph", prop: "URIRef", roots: Optional[Set["Node"]] = None
) -> Set["Node"]:
    """
    Find the roots in some sort of transitive hierarchy.

    find_roots(graph, rdflib.RDFS.subClassOf)
    will return a set of all roots of the sub-class hierarchy

    Assumes triple of the form (child, prop, parent), i.e. the direction of
    RDFS.subClassOf or SKOS.broader

    """

    non_roots: Set[Node] = set()
    if roots is None:
        roots = set()
    for x, y in graph.subject_objects(prop):
        non_roots.add(x)
        if x in roots:
            roots.remove(x)
        if y not in non_roots:
            roots.add(y)
    return roots

def test_find_roots():
    """Check the correctness of find_roots
    """
    assert find_roots(rdflib.graph.Graph(), rdflib.RDFS.subClassOf) == set()