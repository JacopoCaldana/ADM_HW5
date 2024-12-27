def create_adjacency_list(flights, n):
    """
    Creates an adjacency list representation of a graph from a list of flights.

    Args:
        flights (list of lists): Each element is a list [u, v, cost], representing
            a flight from node `u` to node `v` with a cost `cost`.
        n (int): Total number of nodes in the graph.

    Returns:
        list of lists: The adjacency list where each index `i` represents a node,
        and contains a list of [neighbor, cost] pairs for all outgoing flights.
    """
    # Initialize an empty list for each node
    adj_list = [[] for _ in range(n)]
    for u, v, cost in flights:
        # Append the neighbor and cost as a pair to the adjacency list of `u`
        adj_list[u].append([v, cost])
    return adj_list


def min_cost_with_max_K_edges_DFS(G, currentNode, destination, max_stops, current_cost, min_cost_so_far, visited_nodes):
    """
    Performs a depth-first search (DFS) to find the minimum cost to travel from currentNode to destination
    within the constraints of at most maxStops edges.

    Args:
        G (list of lists): The adjacency list representation of the graph;
        current_node (int): The current node being processed;
        destination (int): The destination node;
        max_stops (int): The maximum number of edges allowed in the route;
        current_cost (int): The accumulated cost of the current route;
        min_cost_so_far (int): The minimum cost found so far during the search;
        visited_nodes (set): The set of nodes already visited in the current DFS path.

    Returns:
        int: The updated minimum cost to travel from currentNode to destination within the given constraints.
    """
    # Initialize the updated minimum cost with the previous minimum cost
    updated_min_cost = min_cost_so_far

    # If the destination is reached, update and return the minimum cost
    if currentNode == destination:
        return min(min_cost_so_far, current_cost)

    # If no more stops are allowed, terminate the search
    if max_stops < 0:
        return min_cost_so_far

    # Mark the current node as visited
    visited_nodes.add(currentNode)

    # Explore all neighbors of the current node
    for neighbor, edgeCost in G[currentNode]:
        # Proceed only if the neighbor is not visited and the total cost is less than the current minimum
        if neighbor not in visited_nodes and current_cost + edgeCost < updated_min_cost:
            updated_min_cost = min_cost_with_max_K_edges_DFS(
                G, neighbor, destination, max_stops - 1, current_cost + edgeCost, updated_min_cost, visited_nodes
            )

    # Unmark the current node as visited
    visited_nodes.remove(currentNode)
    
    return updated_min_cost


def find_cheapest_route_DFS(n, flights, src, dst, k):
    """
    Finds the minimum cost to travel from a source node to a destination node
    using at most k stops (k+1 flights).

    Args:
        n (int): Total number of nodes in the graph.
        flights (list of lists): Each element is a list [u, v, cost], representing
            a flight from node `u` to node `v` with a cost `cost`.
        src (int): The source node.
        dst (int): The destination node.
        k (int): The maximum number of stops allowed.

    Returns:
        int: The minimum cost to travel from src to dst. Returns -1 if no valid route exists.
    """
    # Build the adjacency list
    G = create_adjacency_list(flights, n)

    # Initialize the initial minimum cost as infinity
    initial_min_cost = float('inf')

    # Set to track visited nodes
    visited = set()

    # Perform a depth-first search to calculate the minimum cost
    calculated_min_cost = min_cost_with_max_K_edges_DFS(G, src, dst, k, 0, initial_min_cost, visited)

    # Return the result. If no valid route is found, return -1.
    if calculated_min_cost != float('inf'):
        return calculated_min_cost

    return -1

def min_cost_with_max_k_edges_pol(G, src, dst, k):
    """
    Finds the minimum cost to travel from 'source' to 'destination'
    using at most 'max_edges' edges in a graph with non-negative weights.

    Args:
        - G (list of lists): The adjacency list representation of the graph;
        - src (int): source node (integer index);
        - dst (int): destination node (integer index);
        - k (int): maximum number of edges allowed (integer).

    Returns:
        - int: A numeric value representing the minimum cost, or float('inf') if no path with at most k edges exists.
    """
    
    num_nodes = len(G)
    INF = float('inf')
    
    # min_cost_per_edge[i][v] = minimum cost to reach node 'v' using at most 'i' edges.
    min_cost_per_edge = [[INF] * num_nodes for _ in range(k + 2)]
    
    # With 0 edges, the only reachable node from the source is the source itself.
    min_cost_per_edge[0][src] = 0
    
    # Update distances for each number of edges from 1 to max_edges + 1
    for edge_count in range(1, k + 2):
        # Copy the previous row so min_cost_per_edge[edge_count][.] starts as a copy of min_cost_per_edge[edge_count - 1][.]
        min_cost_per_edge[edge_count] = min_cost_per_edge[edge_count - 1][:]
        
        # For each node 'u'
        for u in range(num_nodes):
            # If the cost to reach 'u' (using edge_count - 1 edges) is infinite, 
            # it means 'u' is not reachable with edge_count - 1 edges. 
            # Consequently, it cannot be reachable with edge_count either, so we skip this node.
            if min_cost_per_edge[edge_count - 1][u] != INF:
                # For each neighbor 'v' of the current node 'u':
                for (v, weight) in G[u]:
                    # Calculate the cost of reaching 'v' through 'u' using edge_count edges.
                    new_cost = min_cost_per_edge[edge_count - 1][u] + weight
                    # If this new cost is less than the current recorded cost to reach 'v' with edge_count edges, update min_cost_per_edge[edge_count][v] with the new cost.
                    if new_cost < min_cost_per_edge[edge_count][v]:
                        min_cost_per_edge[edge_count][v] = new_cost
    
    # The minimum cost to reach destination with at most max_edges edges is the minimum among min_cost_per_edge[edge_count][destination] for edge_count in [0, max_edges + 1].
    min_cost = min(min_cost_per_edge[edge_count][dst] for edge_count in range(k + 2))
    return min_cost

def find_cheapest_route_pol(n, flights, src, dst, k):
    """
    Finds the minimum cost to travel from a source node to a destination node
    using at most k stops (k+1 flights).

    Args:
        n (int): Total number of nodes in the graph.
        flights (list of lists): Each element is a list [u, v, cost], representing
            a flight from node `u` to node `v` with a cost `cost`.
        src (int): The source node.
        dst (int): The destination node.
        k (int): The maximum number of stops allowed.

    Returns:
        int: The minimum cost to travel from src to dst. Returns -1 if no valid route exists.
    """
    # Build the adjacency list
    G = create_adjacency_list(flights, n)

    # Perform a depth-first search to calculate the minimum cost
    calculated_min_cost = min_cost_with_max_k_edges_pol(G, src, dst, k)

    # Return the result. If no valid route is found, return -1.
    if calculated_min_cost != float('inf'):
        return calculated_min_cost

    return -1


from heapq import heappush, heappop

def min_cost_with_max_K_edges_Dijkstra(G, src, dst, k):
    """
    Finds the minimum cost to travel from src to dst with at most k stops using a Dijkstra-like approach.
    
    Args:
        G (list of lists): Adjacency list representation of the graph;
        src (int): Starting node;
        dst (int): Destination node;
        k (int): Maximum number of stops allowed.

    Returns:
        int: Minimum cost to reach the destination, or -1 if no valid path exists.
    """
    # Step 1: Initialize minDistanceK and priority_queue
    min_distance_K = [float('inf')] * len(G)
    min_distance_K[src] = 0
    priority_queue = [(0, src, 0, {src})]  # (current_cost, current_node, current_stops, visited_set)

    # Step 2: Process the queue
    while priority_queue:
        current_cost, current_node, current_stops, current_visited = heappop(priority_queue)

        # If stops are within the allowed limit
        if current_stops <= k + 1:
            # If destination is reached, update the cost and exit
            if current_node == dst:
                min_distance_K[dst] = current_cost
                break

            # Explore neighbors
            for neighbor, edge_cost in G[current_node]:
                # Check if the neighbor has not been visited in the current path
                if neighbor not in current_visited:
                    new_cost = current_cost + edge_cost

                    # Update the cost if it's better or fewer stops are needed
                    if min_distance_K[neighbor] > new_cost or current_stops + 1 < k + 1:
                        min_distance_K[neighbor] = new_cost
                        new_visited = current_visited | {neighbor}
                        heappush(priority_queue, (new_cost, neighbor, current_stops + 1, new_visited))

    # Step 3: Return the result
    return min_distance_K[dst]

def find_cheapest_route_Dijkstra(n, flights, src, dst, k):
    """
    Main function to find the cheapest price using the modified BFS algorithm.
    
    Args:
        n (int): Number of nodes in the graph.
        flights (list): List of flights as [from, to, cost].
        src (int): Starting node.
        dst (int): Destination node.
        k (int): Maximum number of stops allowed.
    
    Returns:
        int: Minimum cost to reach the destination, or -1 if no valid path exists.
    """
    # Build the graph as an adjacency list
    G = create_adjacency_list(flights, n)
    
    # Call the BFS function
    min_cost = min_cost_with_max_K_edges_Dijkstra(G, src, dst, k)
    if min_cost != float('inf'):
        return min_cost
    return -1
