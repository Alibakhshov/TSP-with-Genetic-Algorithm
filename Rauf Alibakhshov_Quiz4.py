import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph as a dictionary of nodes and their neighbors with associated costs
graph = {
    'A': {'B': 6, 'F': 3},
    'B': {'A': 6, 'C': 3, 'D': 2},
    'C': {'B': 3, 'E': 5, 'D': 1},
    'D': {'B': 2, 'E': 8, 'C': 1},
    'E': {'C': 5, 'D': 8, 'J': 5, 'I': 5},
    'F': {'A': 3, 'H': 7, 'G': 1},
    'G': {'I': 3, 'F': 1},
    'H': {'F': 7, 'I': 2},
    'I': {'G': 3, 'H': 2, 'J': 3, 'E': 5},
    'J': {'E': 5, 'I': 3}
}

# Heuristic values for each node
heuristics = {
    'A': 10, 'B': 8, 'C': 5, 'D': 7, 'E': 3,
    'F': 6, 'G': 5, 'H': 3, 'I': 1, 'J': 10
}

# A* search function
def astar(graph, heuristics, start, goal):
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, (heuristics[start], 0, start, [start]))

    while open_list:
        _, current_g, current_node, path = heapq.heappop(open_list)
        closed_list.add(current_node)

        if current_node == goal:
            return path, current_g

        for neighbor, cost in graph[current_node].items():
            if neighbor in closed_list:
                continue

            neighbor_g = current_g + cost
            neighbor_h = heuristics[neighbor]
            neighbor_f = neighbor_g + neighbor_h

            heapq.heappush(open_list, (neighbor_f, neighbor_g, neighbor, path + [neighbor]))

    return None, None

# Visualize the graph
def visualize_graph(graph, path=None):
    G = nx.Graph()
    for node, neighbors in graph.items():
        G.add_node(node)
        for neighbor, cost in neighbors.items():
            G.add_edge(node, neighbor, weight=cost)

    pos = nx.spring_layout(G)  # You can choose a different layout if needed

    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black')

    if path:
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()

# Main function to handle user input
if __name__ == "__main__":
    # Prompt the user for the start and goal nodes
    start_node = input("Enter the start node: ").strip().upper()
    goal_node = input("Enter the goal node: ").strip().upper()

    if start_node not in graph or goal_node not in graph:
        print("Invalid start or goal node. Please enter a valid node from the graph.")
    else:
        path, cost = astar(graph, heuristics, start_node, goal_node)

        if path:
            print(f"The path from {start_node} to {goal_node} is: {' -> '.join(path)} with a total cost of {cost}")
            visualize_graph(graph, path)
        else:
            print("No path found.")
