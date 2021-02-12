import bisect
import math

def helperFindMin(dist, visited):
    temp = math.inf
    for i in range(len(dist)):
        if dist[i] < temp and visited[i] == False:
            temp = dist[i]
            temp_i = i
    return temp_i

def dijkstra(vlist, source, dest):
    dist = [math.inf] * len(vlist)
    dist[source] = 0
    visited = [False] * len(vlist)

    while False in visited:
        cur_i = helperFindMin(dist, visited)
        cur = vlist.get(cur_i)
        visited[cur_i] = True
        for edge in cur.edges:
            target_i = edge.v2 if edge.v1 == cur_i else edge.v1
            if visited[target_i] == False and dist[target_i] > dist[cur_i] + edge.distance:
                dist[target_i] = dist[cur_i] + edge.distance
    return dist[dest] if dist[dest] != math.inf else None

# calculate heuristic value for all nodes
def heuristic(vlist, dest):
    heur = [0] * len(vlist)
    dest_square = vlist.get(dest).square
    for k, v in vlist.items(): 
        val = eucli_dist(v.square, dest_square)
        heur[k] = val
    return heur

def eucli_dist(s1, s2):
    s1x = (s1 % 10) * 100
    s2x = (s2 % 10) * 100
    s1y = int(s1 / 10) * 100
    s2y = int(s2 / 10) * 100
    d = math.sqrt((s2x - s1x)**2 + (s2y - s1y)**2)
    return d

# check if the current fringe is already in the fringe list. If yes, replace the existing fringe if it have a lower fn.
def add_fringe(fringe, target, fn_t, gn_t):
    for fn, i, gn in fringe:
        if i == target:
            if fn < fn_t:
                return
            else:
                fringe.remove((fn, i, gn))
    bisect.insort(fringe, (fn_t, target, gn_t))

def a_heuristic(vlist, source, dest):
    if source == dest:
        return 0
    closed = [False] * len(vlist)
    fringe = []
    cost = 0 # if cost == 0, it means that no destination is found yet.
    heur = heuristic(vlist, dest)
    fringe.append((heur[source], source, cost ))
    # fringe input: f(n), vertex id, g(n)
    while len(fringe) > 0:
        elem = fringe.pop(0)
        fn, cur_i, gn = elem
        if cost != 0 and fn >= cost: # end the loop
            break;
        cur = vlist.get(cur_i)

        for edge in cur.edges:
            target_i = edge.v2 if edge.v1 == cur_i else edge.v1
            if target_i == dest:
                if cost==0 or gn+edge.distance < cost: # if found a destination, compare the distance
                    cost = gn + edge.distance 
            elif closed[target_i] == False:
                gn_t = gn + edge.distance
                fn_t = gn_t + heur[target_i]
                if cost==0 or fn_t < cost:
                    add_fringe(fringe, target_i, fn_t, gn_t)
        closed[cur_i] = True        

    return cost if cost != 0 else None
