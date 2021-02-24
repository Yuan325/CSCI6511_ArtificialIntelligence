import math

def backtrack(vlist, color):
    csp_list={}
    for k in vlist.keys():
        csp_list[k] = -1
    return recursion(csp_list, vlist, color)

def recursion(csp_list, vlist, color):
    if -1 not in csp_list.values():
        return csp_list
    cur = mrv(csp_list, vlist, color)
    avoid = []
    val = lcv(cur, csp_list, color, avoid) 
    while val != -1 and len(avoid) != len(cur.domains): # while there are available values
        csp_list[cur.vid] = val
        changed = ac3(cur, val, csp_list)
        res = recursion(csp_list, vlist, color)
        if res != None:
            return res
        return_domain(changed, val, csp_list)
        csp_list[cur.vid] = -1
        avoid.append(val)
        val = lcv(cur, csp_list, color, avoid)
    return None

# minimum remaining values
# pick the vertex that have fewest values available
# break ties with vertex that have more neighbors
def mrv(csp_list, vlist, color):
    dom_n = color + 1
    next_v = None;
    for k, v in csp_list.items():
        if v == -1:
            cur = vlist.get(k)
            occur = len(cur.domains)
            if occur == dom_n and len(cur.adjs) > len(next_v.adjs):
                next_v = cur
            elif occur < dom_n:
                next_v = cur    
    return next_v

# least constraint value
# if there's only 1 value left, pick that
# pick value that rules out fewest values in the remaining neighboring vertex
def lcv(cur, csp_list, color, avoid):
    temp = [0] * color
    least_block = math.inf
    value = -1
    if len(cur.domains) == 1:
        if cur.domains[0] in avoid:
            return value
        return cur.domains[0]
    for i in cur.domains:
        if i not in avoid:
            block = 0
            for adj in cur.adjs:
                if i in adj.domains:
                    block += 1
            if block < least_block:
                value = i
                least_block = block
    return value

# constraint propagation
# check for arc consistency with adjacent vertex
# remove assigned value from adjacent vertex's domains
# if there's only 1 available value after removal, assign that value to the vertex
def ac3(cur, val, csp_list):
    changed = []
    for adj in cur.adjs:
        if csp_list[adj.vid] == -1 and val in adj.domains:
            adj.domains.remove(val)
            changed.append(adj)
            if len(adj.domains) == 1:
                csp_list[adj.vid] = adj.domains[0]
    return changed

# this is only called when backtrack happens
# place removed values back to the vertex
def return_domain(changed, val, csp_list):
    for v in changed:
        v.domains.append(val)
        csp_list[v.vid] = -1
    return
