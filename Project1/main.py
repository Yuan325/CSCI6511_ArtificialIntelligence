import graph as g
from search import dijkstra, a_heuristic
from timeit import default_timer as timer

def main():
    f = open("p1_graph.txt", "r")
    Lines = f.readlines()
    f.close()
    vlist, source, dest = readFile(Lines)
    print("Path from ", source, " to ", dest)
    # uninformed search: dijkstra
    start = timer()
    path_d = dijkstra(vlist, source, dest)
    end = timer()
    d_time = end - start
    print("\nDijkstra Algorithm")
    print("Path Distance: ", path_d, "\nTime Taken: ", d_time)
    # informed search: a* heuristic search
    start = timer()
    path_h = a_heuristic(vlist, source, dest)
    end = timer()
    a_time = end - start
    print("\nA* Heuristic Search Algorithm")
    print("Path Distance: ", path_h, "\nTime Taken: ", a_time)
    
def readFile(Lines):
    vlist = {}
    source = 0
    dest = 0
    for line in Lines:
        if line.startswith("#"):
            continue
        else:
            x = line.strip("\n").split(",")
            if len(x) == 2:
                if x[0] == "S":
                    source = int(x[1])
                elif x[0] == "D":
                    dest = int(x[1])
                else:
                    x[0] = int(x[0])
                    x[1] = int(x[1])
                    v = g.vertices(x[0], x[1])
                    vlist[x[0]] = v
            elif len(x) == 3:
                x[0] = int(x[0])
                x[1] = int(x[1])
                x[2] = float(x[2])
                v1 = vlist.get(x[0])
                v2 = vlist.get(x[1])
                e = g.edges(x[0], x[1], x[2])
                v1.add_edge(e)
                v2.add_edge(e)
    return vlist, source, dest

if __name__ == "__main__":
    main()
