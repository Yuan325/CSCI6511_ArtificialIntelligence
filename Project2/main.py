from search import solve_csp 

def main():
    f = open("input/input44line.txt", "r")
    Lines = f.readlines()
    f.close()
    print("Reading files")
    adjs, doms, arcs, color = readFile(Lines)
    print("Done reading. Starting csp graph coloring.")
    res = solve_csp(adjs, doms, arcs, color)
    print("Result of CSP Graph Coloring: ")
    if res == None:
        print("No solution was found.")
    else:
        print(res)
    
def readFile(Lines):
    adjs = {}
    doms = {}
    arcs = []
    color = -1
    for line in Lines:
        if line.startswith("#"):
            continue
        elif color == -1:
            color = int(line.partition("=")[2])
        else:
            x = line.strip("\n").split(",")
            v1 = int(x[0])
            v2 = int(x[1])
            if v1 not in adjs:
                adjs[v1] = []
                doms[v1] = []
                for i in range(color):
                    doms.get(v1).append(i)
            if v2 not in adjs:
                adjs[v2] = []
                doms[v2] = []
                for i in range(color):
                    doms.get(v2).append(i)
            if v2 not in adjs.get(v1):
                adjs.get(v1).append(v2)
                adjs.get(v2).append(v1)
                arcs.append((v1, v2))
                arcs.append((v2, v1))
    return adjs, doms, arcs, color

if __name__ == "__main__":
    main()
