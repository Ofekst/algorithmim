import random

def create_graph(num_vertices:int, num_edges:int) -> (dict[int,list[int]],list[int]):
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

def print_graph(graph:dict):
    """
    Prints the graph's adjacency list
    :param graph: The adjacency list of the graph (dictionary)
    """
    print("Full graph (Vertex -> [(connected vertex, weight)]):")
    for vertex, edges in graph.items():
        print(f"{vertex} -> {[(v, w) for v, w in edges]}")

def main():
    num_vertices = 6
    num_edges = 8

    result = create_graph(num_vertices, num_edges)
    if result:
        graph, edges = result
        print_graph(graph)

        print("\nEdge list:")
        for v1, v2, weight in edges:
            print(f"{v1} --({weight})-- {v2}")

if __name__ == "__main__":
    main()
