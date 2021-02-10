class vertices:
    def __init__ (self, vertex_id, square_id):
        self.vid = vertex_id
        self.square = square_id
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

class edges:
    def __init__ (self, v1, v2, distance):
        self.v1 = v1
        self.v2 = v2
        self.distance = distance
