import math
import copy

def solve_csp(adjs, doms, arcs, color):
    csp_list={}
    for k in adjs.keys():
        csp_list[k] = -1
    return backtracking(csp_list, adjs, doms, arcs, color)

def backtracking(csp_list, adjs, doms, arcs, color):
    if -1 not in csp_list.values():
        return csp_list
    ac3(copy.deepcopy(arcs), adjs, doms)
    cur = mrv(csp_list,adjs, doms, color)
    val = lcv(cur, csp_list, adjs, doms, color) 
    while val != -1: # while there are available values to pick from
        csp_list[cur] = val
        changed = filtering(cur, csp_list, adjs, doms, val) # once change is made, filter and forward check
        res = backtracking(copy.deepcopy(csp_list), adjs, copy.deepcopy(doms), arcs, color) 
        if res != None:
            return res
        return_domain(changed,doms, val, csp_list) 
        csp_list[cur] = -1
        doms.get(cur).remove(val)
        val = lcv(cur, csp_list, adjs, doms, color) # pick next available value
    return None

# constraint propagation - arc consistency
# queue implemented with List in Python
def ac3(arcs, adjs, doms):
    while len(arcs) != 0:
        xi, xj = arcs.pop(0)
        if remove_inconsistent_values(xi, xj, doms):
            for adj in adjs.get(xi):
                arcs.append((adj, xi))
    return

def remove_inconsistent_values(xi, xj, doms):
    removed = False
    for dom in doms.get(xi):
        if dom in doms.get(xj) and len(doms.get(xj)) == 1:
            doms.get(xi).remove(dom)
            removed = True
    return removed

# minimum remaining values
# pick the vertex that have fewest values available
# break ties with vertex that have more neighbors
def mrv(csp_list, adjs, doms, color):
    dom_n = color + 1
    next_v = None;
    for k, v in csp_list.items():
        if v == -1:
            occur = len(doms.get(k))
            if (occur == dom_n and len(adjs.get(k)) > len(adjs.get(next_v))) or occur < dom_n:
                next_v = k
    return next_v

# least constraint value
# if there's only 1 value left, pick that
# pick value that rules out fewest values in the remaining neighboring vertex
def lcv(cur, csp_list, adjs, doms, color):
    temp = [0] * color
    least_block = math.inf
    value = -1
    if len(doms.get(cur)) == 0: 
        return value
    if len(doms.get(cur)) == 1:
        return doms.get(cur)[0]
    for v in doms.get(cur):
        block = 0
        for adj in adjs.get(cur):
            if v in doms.get(adj):
                block += 1
        if block < least_block:
            value = v
            least_block = block
    return value

# constraint propagation - filtering / forward checking
# remove assigned value from adjacent vertex's domains
# if there's only 1 available value after removal, assign that value to the vertex
def filtering(cur, csp_list, adjs, doms, val):
    changed = []
    for adj in adjs.get(cur):
        domains = doms.get(adj)
        if csp_list[adj] == -1 and val in domains:
            domains.remove(val)
            changed.append(adj)
            if len(domains) == 1:
                csp_list[adj] = domains[0]
    return changed

# this is only called when backtrack happens
# place removed values back to the vertex
def return_domain(changed, doms, val, csp_list):
    for v in changed:
        doms.get(v).append(val)
        csp_list[v] = -1
    return
