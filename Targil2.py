def add_edge(mst_tree: dict, edge):
    v, u, w = edge
    # # maby add check to see if the vertex is not new
    # add check if the edge exists
    mst_tree[v].append((u, w))
    mst_tree[u].append((v, w))
    return mst_tree

def remove_edge(mst_tree: dict, edge):
    v, u, w = edge

    mst_tree[v].remove((u, w))
    mst_tree[u].remove((v, w))

    return mst_tree

def remove_edge_from_mst(mst, edge_to_remove):
    u, v, w = edge_to_remove
    new_mst = []

    for edge in mst:
        a, b, weight = edge
        if (a == u and b == v and weight == w) or (a == v and b == u and weight == w):
            continue  # skip the edge we want to remove
        new_mst.append(edge)

    return new_mst

def exchange_edge(mst_tree: dict, edge_to_exchange, new_edge):
    if new_edge not in mst_tree:
        tree_with_new_edge = add_edge(mst_tree, new_edge)
        tree_aftrer_removing_edge = remove_edge(tree_with_new_edge, edge_to_exchange)
        
        return tree_aftrer_removing_edge

def find_cycle_fast(mst, new_edge):
    graph = {}         # מילון רגיל
    edge_weights = {}  # מחזיק את המשקלים של הצלעות

    # בניית גרף שכונתי מה-MST
    for u, v, w in mst:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
        edge_weights[(u, v)] = w
        edge_weights[(v, u)] = w

    u, v, w = new_edge
    visited = set()

    def dfs(current, target, curr_path):
        if current == target:
            return curr_path
        visited.add(current)
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                result = dfs(neighbor, target, curr_path + [(current, neighbor, edge_weights[(current, neighbor)])])
                if result:
                    return result
        return None

    cycle_path = dfs(u, v, [])
    if cycle_path is None:
        return []

    cycle_path.append(new_edge)
    return cycle_path


# def add_edge_to_mst_tree(mst_tree: list, edge):
#     cycle_path = find_cycle_fast(mst_tree, edge)
    
#     max_edge = max(cycle_path, key=lambda edge: edge[2])
#     if edge == max_edge:
#         return mst_tree # changes nothing
#     else:
#         return remove_edge_from_mst(mst_tree, max_edge)
    
def add_edge_to_mst_tree(mst_tree: list, edge):
    cycle_path = find_cycle_fast(mst_tree, edge)

    if not cycle_path:
        return mst_tree  # במקרה נדיר שאין מעגל (למרות שצפוי שיהיה) – לא נוגעים

    # מוצא את משקל הצלע הכי גבוהה במעגל
    max_weight = max(e[2] for e in cycle_path)
    
    # בודק את כל הצלעות שהן מקסימום
    max_edges = [e for e in cycle_path if e[2] == max_weight]

    # אם הצלע החדשה היא אחת מהכבדות – אין שיפור, לא מחליפים
    if edge in max_edges:
        return mst_tree

    # בוחר אחת מהכבדות (שהיא לא הצלע החדשה) ומסיר אותה
    edge_to_remove = next(e for e in max_edges if e != edge)
    new_mst = remove_edge_from_mst(mst_tree, edge_to_remove)
    new_mst.append(edge)

    return new_mst
            
            

graph = {0: [(1, 1), (2, 10), (3, 10), (4, 4), (5, 5)],
         1: [(0, 1), (4, 6), (5, 8)], 2: [(0, 10)],
         3: [(0, 10)],
         4: [(1, 6), (5, 10), (0, 4)],
         5: [(4, 10), (1, 8), (0, 5)]}

edges_array = [(0, 1, 1), (1, 4, 6), (0, 2, 10), (0, 3, 10), (4, 5, 10)]

# graph =  {
#     0: [(1, 5), (4, 10), (3, 8)],
#     1: [(0, 5), (2, 7), (3, 8), (4, 3)],
#     2: [(1, 7), (3, 4)],
#     3: [(0, 8), (1, 8), (2, 4)],
#     4: [(0, 10), (5, 2), (1, 3)],
#     5: [(4, 2)]
# }

new_edge = (1, 2, 9)
remove_edge_ofek = (0,1,1)

# print(add_edge(graph, new_edge))
# print(remove_edge(graph, remove_edge_ofek))

# print(exchange_edge(graph, remove_edge_ofek, new_edge))

print(add_edge_to_mst_tree(edges_array, new_edge))