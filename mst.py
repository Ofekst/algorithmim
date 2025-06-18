# Authors: Ofek Streicher - 324826965 & Eyal Zohar - 323091629
import random

def create_graph(num_vertices:int, num_edges:int):
    """
    Creates a connected undirected weighted graph

    First, it builds a spanning tree to guarantee the graph is connected.
    Then, it adds random extra edges (without duplication) until the
    total number of edges equals num_edges.

    :param num_vertices: Number of vertices in the graph
    :param num_edges: Number of edges in the graph
    :return: A tuple:
             - graph: a dictionary representing the adjacency list of the graph
             - edges_array: a list of tuples representing edges
    """
    if num_edges < num_vertices - 1:
        raise ValueError("Error: To ensure a connected graph,"
                         " the number of edges must be at least", num_vertices - 1)

    max_edges = num_vertices * (num_vertices - 1) // 2
    if num_edges > max_edges:
        raise ValueError(f"Too many edges. Maximum for {num_vertices} vertices is {max_edges}.")

    graph = {vertex: [] for vertex in range(num_vertices)}
    edges_array = []
    existing_edges = set()

    # Create a spanning tree
    available_vertices = list(range(1, num_vertices))
    connected_vertices = [0]

    while available_vertices:
        v1 = random.choice(connected_vertices)
        v2 = available_vertices.pop(random.randrange(len(available_vertices)))
        weight = random.randint(1, 10)

        graph[v1].append((v2, weight))
        graph[v2].append((v1, weight))
        edges_array.append((v1, v2, weight))
        existing_edges.add((min(v1, v2), max(v1, v2)))
        connected_vertices.append(v2)

    edge_count = num_vertices - 1

    # Add more edges
    while edge_count < num_edges:
        v1, v2 = random.sample(range(num_vertices), 2)
        edge_key = (min(v1, v2), max(v1, v2))

        if edge_key not in existing_edges:
            weight = random.randint(1, 10)
            graph[v1].append((v2, weight))
            graph[v2].append((v1, weight))
            edges_array.append((v1, v2, weight))
            existing_edges.add(edge_key)
            edge_count += 1

    return graph, edges_array

def print_full_graph(graph:dict):
    """
    Prints the graph's adjacency list
    :param graph: The adjacency list of the graph (dictionary)
    """
    print("Full graph (Vertex -> [(connected vertex, weight)]):")
    for vertex, edges in graph.items():
        print(f"{vertex} -> {[(v, w) for v, w in edges]}")


def prim_algorithm(vertices:list, edges:list[tuple]) -> list[tuple[int, int, int]]:
    """
     The function implements PRIM algorithm
    :param vertices: The adjacency list of the graph (dictionary)
    :param edges: The list of tuples representing edges
    :return: mst graph after prim's algorithm
    """
    mst_graph  = []
    mst_vertices_dict = {vertices[0]}
    edges_with_weights = [(weight, start, end) for start, end, weight in edges]

    edges_with_weights.sort() # This sorts the edges according to their weights

    while len(mst_vertices_dict) < len(vertices):
        for edge in edges_with_weights:
            (weight, start_vertex, end_vertex) = edge
            if (start_vertex in mst_vertices_dict and end_vertex not in mst_vertices_dict or
                    end_vertex in mst_vertices_dict and start_vertex not in mst_vertices_dict):
                mst_graph.append((start_vertex, end_vertex, weight))
                mst_vertices_dict.update([start_vertex, end_vertex])
                break
    return mst_graph

def print_mst_graph(mst:list[tuple[int, int, int]]):
    """
    Prints the mst graph
    :param mst: The mst graph as list of tuples representing edges
    """
    for start, end, weight in mst:
        print(f"{start} - {end} with weight {weight}")

def add_edge_that_does_not_change_mst(mst, vertices):
    """
    Adds an edge between two vertices such that it doesn't
    change the structure of the given MST.

    :param mst: List of tuples representing the MST edges in the form (start_vertex, end_vertex, weight).
    :param vertices: List of all vertices in the graph.
    :return: A tuple (v1, v2, weight) representing the new edge that does not affect the MST.
    """
    while True:
        v1, v2 = random.sample(vertices, 2)
        if not any((v1 == start and v2 == end) or (v1 == end and v2 == start) for start, end, _ in mst):
            path_exists = False
            for start, end, weight in mst:
                if v1 == start or v1 == end or v2 == start or v2 == end:
                    path_exists = True
                    break
            if path_exists:
                weight = max(weight for start, end, weight in mst) + random.randint(1, 10)
                print(f"Adding edge ({v1}, {v2}) with weight {weight}")
                return v1, v2, weight

def add_edge_that_changes_mst(mst, vertices):
    """
    Adds an edge between two vertices that changes the structure of the given MST.

    :param mst: List of tuples representing the MST edges in the form (start_vertex, end_vertex, weight).
    :param vertices: List of all vertices in the graph.
    :return: A tuple (v1, v2, weight) representing the new edge that could replace an edge in the MST.
    """

    while True:
        v1, v2 = random.sample(vertices, 2)
        if not any((v1 == start and v2 == end) or (v1 == end and v2 == start)
                   for start, end, weight in mst):
            weight = min(weight for start, end, weight in mst) - 1
            print(f"Adding edge ({v1}, {v2}) with weight {weight}")
            return v1, v2, weight

def remove_edge_from_tree_list(mst: list, edge_to_remove):
    u, v, w = edge_to_remove
    new_mst = []

    for edge in mst:
        a, b, weight = edge
        if (a == u and b == v and weight == w) or (a == v and b == u and weight == w):
            continue  # skip the edge we want to remove
        new_mst.append(edge)

    return new_mst

def add_edge_to_tree_list(mst: list, new_edge):
    u, v, w = new_edge

    # Check for duplicate in either direction
    for a, b, w in mst:
        if ({a, b} == {u, v}):
            return mst  # Do not add; already exists

    mst.append(new_edge)
    return mst

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
                result = dfs(neighbor, target, curr_path +
                             [(current, neighbor, edge_weights[(current, neighbor)])])
                if result:
                    return result
        return None

    cycle_path = dfs(u, v, [])
    if cycle_path is None:
        return []

    cycle_path.append(new_edge)
    return cycle_path

def exchange_edges_mst_list(mst: list, edge_to_exchange, new_edge):
    tree_with_new_edge = add_edge_to_tree_list(mst, new_edge)
    tree_after_removing_edge = remove_edge_from_tree_list(tree_with_new_edge, edge_to_exchange)
    return tree_after_removing_edge

def update_mst_with_new_edge(mst: list, new_edge):
    cycle_path = find_cycle_fast(mst, new_edge)

    if not cycle_path:
        return mst  # In case there is no cycle

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

    new_mst = exchange_edges_mst_list(mst, edge_to_remove, new_edge)
    return new_mst

def main():
    # vertices_array = ["A" , "B" , "C" , "D" , "E"]
    # edges_array = [
    #     ("A" , "B" , 2),
    #     ("A" , "C" , 3),
    #     ("B" , "C" , 1),
    #     ("B" , "D" , 5),
    #     ("D" , "E" , 1),
    #     ("C" , "E" , 4)
    #
    # ]
    #
    # result = prim_algorithm (vertices_array,edges_array)
    # print("\nThe MST Tree is:")
    # print_mst_graph(result)
    # edge  = ("A" , "B" , 2)
    # new_mst = update_mst_with_new_edge(result , edge)
    # print("\nThe new MST Tree is:")
    # print_mst_graph(new_mst)

    num_vertices = 20
    num_edges = 50

    # Part 1: Create graph with 20 vertices and 50 edges
    result = create_graph(num_vertices, num_edges)
    if result:
        graph, edges = result
        # Part 2: print the full graph
        print_full_graph(graph)

        # Part 3: Find MST and print it
        vertices = list(range(num_vertices))
        mst_graph = prim_algorithm(vertices, edges)
        print("\nThe MST Tree is:")
        print_mst_graph(mst_graph)

        # Part 4: Add new edge that does not change the graph and print the edge
        new_edge_does_not_affect = add_edge_that_does_not_change_mst(mst_graph,vertices)
        print(f"The new edge that does not affect is: ({new_edge_does_not_affect}) ")

        # Part 5: Update the mst and print it
        new_mst = update_mst_with_new_edge(mst_graph,new_edge_does_not_affect)
        print("\nThe new MST Tree after add new edge that does not affect is:")
        print_mst_graph(new_mst)

        # Part 6: Add new edge that changes the graph and print the edge
        new_edge_does_affect = add_edge_that_changes_mst(mst_graph, vertices)
        print(f"The new edge that affects is: ({new_edge_does_affect}) ")

        # Part 7: Update the mst and print it
        new_mst = update_mst_with_new_edge(mst_graph,new_edge_does_affect)
        print("\nThe new MST Tree after add new edge that affects is:")
        print_mst_graph(new_mst)
if __name__ == "__main__":
    main()
