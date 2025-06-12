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
        raise ValueError("Error: To ensure a connected graph, the number of edges must be at least", num_vertices - 1)

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
        if not any((v1 == start and v2 == end) or (v1 == end and v2 == start) for start, end, weight in mst):
            weight = min(weight for start, end, weight in mst) - 1
            print(f"Adding edge ({v1}, {v2}) with weight {weight}")
            return v1, v2, weight

def main():
    vertices_array = ["A" , "B" , "C" , "D" , "E"]
    edges_array = [
        ("A" , "B" , 2),
        ("A" , "C" , 3),
        ("B" , "C" , 1),
        ("B" , "D" , 5),
        ("D" , "E" , 1),
        ("C" , "E" , 4)

    ]

    result = prim_algorithm (vertices_array,edges_array)
    print("\nThe MST Tree is:")
    print_mst_graph(result)

    # num_vertices = 20
    # num_edges = 50
    #
    # result = create_graph(num_vertices, num_edges)
    # if result:
    #     graph, edges = result
    #     print_full_graph(graph)
    #
    #     print("\nEdges list:")
    #     for v1, v2, weight in edges:
    #         print(f"{v1} --({weight})-- {v2}")
    #     mst_graph = prim_algorithm(list(range(num_vertices)), edges)
    #
    #     print("\nThe MST Tree is:")
    #     print_mst_graph(mst_graph)

if __name__ == "__main__":
    main()
