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
    assert vertex3tuple(["A", "B", "C", "D"]) == [("D", "A", "B"), ("A", "B", "C"), ("B", "C", "D"), ("C", "D", "A")]
    