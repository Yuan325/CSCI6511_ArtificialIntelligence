import math
import copy


def solve_csp(n, doms, arcs, landscape, tiles, targets):
    csp_list={}
    for i in range(n):
        csp_list[i] = ""
    return backtracking(csp_list, doms, arcs, landscape, tiles, targets)

def backtracking(csp_list, doms, arcs, landscape, tiles, targets):
    if "" not in csp_list.values() and targets.get(1) == 0 and targets.get(2) == 0 and targets.get(3) == 0 and targets.get(4) == 0:
        return csp_list
    #ac3()
    count = 0
    for c in csp_list.values():
        if c == "":
            count += 1
    #print(count)
    cur = mrv(csp_list, doms)
    #print(cur, csp_list) 
    if cur == None:
        return None
    val = lcv(tiles, doms.get(cur))
    while val != "" and cur != None:
        #print(cur," ", val,  " ", doms.get(cur))
        csp_list[cur] = val
        t_targets = deductTargets(landscape, copy.deepcopy(targets), cur, val)
        if t_targets == None:
            return None
        tiles[val] = tiles.get(val) - 1
        changed = []
        if tiles[val] == 0:
            doms = removeDomain(cur, doms, val)

        res = backtracking(copy.deepcopy(csp_list), copy.deepcopy(doms), arcs, landscape, copy.deepcopy(tiles), t_targets) 
        if res != None:
            return res

        tiles[val] = tiles.get(val) + 1
        doms = returnDomain(cur, doms, val)
        csp_list[cur] = ""
        doms.get(cur).remove(val)
        #print(cur, csp_list)
        #print(doms.get(cur))
        
        val = lcv(tiles, doms.get(cur))
    return None


def ac3(n, arcs, doms):
    while len(arcs) != 0:
        xi, xj = arcs.pop(0)
        if remove_inconsistent_values(xi, xj, doms):
            for adj in range(n):
                if adj != xi:
                    arcs.append((adj, xi))
    return

def remove_inconsistent_values(xi, xj, doms):
    removed = False
    for dom in doms.get(xi):
        if dom in doms.get(xj) and len(doms.get(xj)) == 1:
            doms.get(xi).remove(dom)
            removed = True
    return removed

# could be improved
def mrv(csp_list, doms):
    dom_n = 4
    next_v = None
    for k, v in csp_list.items():
        if v == "":
            occur = len(doms.get(k))
            if occur < dom_n:
                next_v = k
    return next_v

# least constraining value
# pick value that still has the most
# prioritizing FB -> OB -> EL since FB will leave nothing visible, hence leaving more chances for other tiles
def lcv(tiles, c_doms):
    if len(c_doms) == 0: 
        return ""
    if len(c_doms) == 1:
        return c_doms[0]
    val = c_doms[0]
    temp = tiles.get(val)
    t2 = "FULL_BLOCK"
    if tiles.get(t2) > temp and t2 in c_doms:
        temp = tiles.get(t2)
        val = t2
    t2 = "OUTER_BOUNDARY"
    if tiles.get(t2) > temp and t2 in c_doms:
        temp = tiles.get(t2)
        val = t2
    t2 = "EL_SHAPE"
    if tiles.get(t2) > temp and t2 in c_doms:
        temp = tiles.get(t2)
        val = t2
    return val

def removeDomain(cur, doms, val):
    for k in doms.keys():
        if k != cur and val in doms.get(k):
            doms.get(k).remove(val)
    return doms

def returnDomain(cur, doms, val):
    for k in doms.keys():
        if k != cur and val not in doms.get(k):
            doms.get(k).append(val)
    return doms

# if return none, means this is the wrong path
def deductTargets(landscape, targets, cur, val):
    per_row = len(landscape)/4
    row = int(cur/per_row)
    r = int(row * 4)
    c = int((cur - (row*per_row)) * 4)
    if val == "FULL_BLOCK":
        return targets
    else:
        for i in range(r+1, r+3):
            for j in range(c+1, c+3):
                t = landscape[i][j]
                if t != 0:
                    targets[t] = targets.get(t) - 1
                    if targets.get(t) < 0:
                        return None
    if val == "EL_SHAPE":
        for i in range(r+1, r+4):
            t = landscape[i][c+3]
            if t != 0:
                targets[t] = targets.get(t) -1
                if targets.get(t) < 0:
                    return None
        for j in range(c+1, c+3):
            t = landscape[r+3][j]
            if t != 0:
                targets[t] = targets.get(t) -1
                if targets.get(t) < 0:
                    return None
    return targets

