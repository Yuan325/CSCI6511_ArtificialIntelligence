import graph as g
from search import backtrack

def main():
    f = open("input/input95line.txt", "r")
    Lines = f.readlines()
    f.close()
    print("Reading files")
    color, vlist = readFile(Lines)
    print("Done reading. Starting csp graph coloring.")
    res = backtrack(vlist, color)
    print("Result of CSP Graph Coloring: ")
    if res == None:
        print("No solution was found.")
    else:
        print(res)
    
def readFile(Lines):
    vlist = {}
    color = -1
    for line in Lines:
        if line.startswith("#"):
            continue
        elif color == -1:
            color = int(line.partition("=")[2])
        else:
            x = line.strip("\n").split(",")
            x[0] = int(x[0])
            x[1] = int(x[1])
            v1 = g.Vertices(x[0], color) if x[0] not in vlist else vlist.get(x[0])
            v2 = g.Vertices(x[1], color) if x[1] not in vlist else vlist.get(x[1])
            vlist[x[0]] = v1
            vlist[x[1]] = v2
            if v2 not in v1.adjs:
                v1.add_adj(v2)
                v2.add_adj(v1)
    return color, vlist

if __name__ == "__main__":
    main()
