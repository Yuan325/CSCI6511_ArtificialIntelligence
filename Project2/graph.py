class Vertices:
    def __init__ (self, vertex_id, color):
        self.vid = vertex_id
        self.adjs = []
        self.domains = []
        for i in range(color):
            self.domains.append(i)

    def add_adj(self, v2):
        self.adjs.append(v2)

