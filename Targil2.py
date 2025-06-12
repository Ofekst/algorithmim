from mst import create_graph, print_full_graph

# def add_edge_from_mst_dict(mst: dict, edge):
#     v, u, w = edge
#     mst[v].append((u, w))
#     mst[u].append((v, w))
#     return mst

# def remove_edge_from_mst_dict(mst: dict, edge):
#     v, u, w = edge

#     mst[v].remove((u, w))
#     mst[u].remove((v, w))

#     return mst

def remove_edge_from_mst_list(mst: list, edge_to_remove):
    u, v, w = edge_to_remove
    new_mst = []

    for edge in mst:
        a, b, weight = edge
        if (a == u and b == v and weight == w) or (a == v and b == u and weight == w):
            continue  # skip the edge we want to remove
        new_mst.append(edge)

    return new_mst

def add_edge_from_mst_list(mst: list, new_edge):
    u, v, w = new_edge

    # Check for duplicate in either direction
    for a, b, w in mst:
        if ({a, b} == {u, v}):
            return mst  # Do not add; already exists

    mst.append(new_edge)
    return mst

def exchange_edge(mst: list, edge_to_exchange, new_edge):
    tree_with_new_edge = add_edge_from_mst_list(mst, new_edge)
    tree_aftrer_removing_edge = remove_edge_from_mst_list(tree_with_new_edge, edge_to_exchange)
    return tree_aftrer_removing_edge

def find_cycle_fast(mst, new_edge):
    graph = {}       
    edge_weights = {}

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
    
def add_edge_to_mst(mst: list, new_edge):
    cycle_path = find_cycle_fast(mst, new_edge)

    if not cycle_path:
        return mst # In case there is no cycle
    
    max_weight_in_cycle = max(edge[2] for edge in cycle_path)
    max_edges_in_cycle = [edge for edge in cycle_path if edge[2] == max_weight_in_cycle]

    # In case the bew edge is one of the max edge, dont do anything
    if new_edge in max_edges_in_cycle:
        return mst

    edge_to_remove = None
    for edge in max_edges_in_cycle:
        if edge != new_edge:
            edge_to_remove = edge
            break
    
    new_mst = exchange_edge(mst, edge_to_remove, new_edge)
    return new_mst
            
            
# # edges_array = [(0, 1, 1), (1, 4, 6), (0, 2, 10), (0, 3, 10), (4, 5, 10)]
# graph, edges_array = create_graph(6, 8)


# new_edge = (1, 2, 10)
# remove_edge_ofek = (0, 1, 1)

# print_graph(graph)

# print("New graph")
# print(exchange_edge(edges_array, remove_edge_ofek, new_edge))


# # print(add_edge_to_mst(edges_array, new_edge))
# # print(add_edge(graph, new_edge))
# # print(remove_edge(graph, remove_edge_ofek))

