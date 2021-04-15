from search import solve_csp 
import re

def main():
    f = open("inputs/tilesproblem_1327003784879400.txt", "r")
    Lines = f.readlines()
    f.close()
    print("Reading files")
    landscape, tiles, targets = readFile(Lines)
    n = int(len(landscape)*len(landscape)/16)
    doms = getDoms(n)
    print("Done reading. Starting csp for tile placement.")
    res = solve_csp(n, doms, landscape, tiles, targets)
    print("Result of CSP Tile Placement: ")
    if res == None:
        print("No solution was found.")
    else:
        print(res)

def readFile(Lines):
    landscape = []
    tiles = {}
    OUTER_BOUNDARY = EL_SHAPE = FULL_BLOCK = 0
    targets={}
    Lines = iter(Lines)

    while True:
        try:
            l = next(Lines)
            if "# Landscape" in l:
                l = next(Lines)
                while "#" not in l and l != "\n":
                    temp = l.strip("\n")
                    row = []
                    for c in temp[::2]:
                        if c == " ":
                            row.append(0)
                        else:
                            row.append(int(c))
                    landscape.append(row)
                    l=next(Lines)
            elif "# Tiles:" in l:
                l = next(Lines)
                temp = re.sub('[{} \n]', '', l)
                temp = temp.split(',')
                for t in temp:
                    t2 = t.split("=")
                    tiles[t2[0]] = int(t2[1])
            elif "# Targets" in l:
                for i in range(1,5):
                    l = next(Lines)
                    targets[i] = int(l.partition(":")[2])
                break

        except StopIteration:
            break
    return landscape, tiles, targets 

def getDoms(n):
    doms = {}
    for i in range(n):
        doms[i] = ["FULL_BLOCK", "OUTER_BOUNDARY", "EL_SHAPE"]
    return doms

if __name__ == "__main__":
    main()
