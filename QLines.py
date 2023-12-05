



class DCEL:
    """A doubly-connected edge list (DCEL) is a data structure to represent a subdivision of the plane.

    The purpose of this data structure is to represent a planar subdivision and efficiently:
        Traverse the boundary of a given face.
        Access one face from an adjacent one.
        Or visit all the edges of a given vertex.

    Attributes:
        vertexRecord: a list of dictionaries to represent the vertices of the arrangement. Each dictionary will have:
                        coordinates: tuple (x, y)
                        incidentEdge: reference to an arbitrary half edge with v as its origin
        faceRecord: a list of disctionaries representing the faces of the arrangement. Each dict will have:
                        outComp: reference to half edge on the outer boundary of f, null if unbounded
                        inComp: reference to a half edge on a hole of a unbounded face
        edgeRecord: a list of dictionaries to represent the half edges of the arrangement. Each dict will have:
                        origin: the vertex origin
                        twin: its twin half-edge, chosen s.t. incident face lies to the left of given half edge
                        incidentFace: a lies to the left of edge e when traversed from origin destination.
                        next: next edge on the boundary of incident face
                        prev: previous edge on the boundary of incident face

    """
    def __init__(self):
        self.vertexRecord = []
        self.faceRecord = []
        self.edgeRecord = []

    def boundingBox(self, v: tuple):
        """Compute a bounding box with corner vertex v"""

    def boundingRegion(self, vList: list[tuple]):
        """Compute the arrangement given the vertices of a polygon"""
