from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import math
def vertex3tuple(vertices):
    """return 3 points for each vertex of the polygon. This will include the vertex and the 2 points on both sides of the vertex::

        polygon with vertices ABCD
        Will return
        DAB, ABC, BCD, CDA -> returns 3tuples
        #A    B    C    D  -> of vertices
    """
    asvertex_list = []
    for i in range(len(vertices)):
        try:
            asvertex_list.append((vertices[i-1], vertices[i], vertices[i+1]))
        except IndexError as e:
           asvertex_list.append((vertices[i-1], vertices[i], vertices[0]))
    return asvertex_list

def test_vertex3tuple():
    """
    Check the corretness of vertex3tuple
    """
    assert set(vertex3tuple(["A", "B", "C", "D"])) == set([("D", "A", "B"), ("A", "B", "C"), ("B", "C", "D"), ("C", "D", "A")])
    assert set(vertex3tuple(["A", "B", "C"])) == set([("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B")])
    assert set(vertex3tuple(["A", "B","C","D","E"])) == set([("E", "A", "B"), ("A", "B", "C"), ("B", "C", "D"), ("C", "D", "E"), ("D", "E", "A")])
    assert set(vertex3tuple(["A", "B","C","D","E","F"])) == set([("F", "A", "B"), ("A", "B", "C"), ("B", "C", "D"), ("C", "D", "E"), ("D", "E", "F"), ("E", "F", "A")])