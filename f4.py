import heapq
import numpy as np
import random
from b1 import nodes, ungerichtet_gewichtet

einsatzstellen = ["F", "G", "H", "J"]

def dijkstra(graph, start_node): #mit Priority Qeue
    num_nodes = len(graph)
    
    # Priority queue will hold tuples of (distance, node)
    pq = [(0, nodes.index(start_node))]  # Start with the start node at distance 0
    unvisited = {node: float('inf') for node in range(num_nodes)}  # Initialize all nodes with inf distance
    unvisited[nodes.index(start_node)] = 0  # Set the start node distance to 0
    
    visited = {}  # This will store the final shortest distance to each node
    parents = {node: None for node in range(num_nodes)}  # To store the path reconstruction info

    while pq:
        # Pop the node with the smallest distance from the priority queue
        current_dist, current_node = heapq.heappop(pq)

        # Skip the node if it has already been visited
        if current_node in visited:
            continue

        # Mark the node as visited
        visited[current_node] = current_dist

        # Check all the neighbors of the current node
        for neighbor, distance in enumerate(graph[current_node]):
            if distance > 0 and neighbor not in visited:  # Only consider unvisited neighbors
                new_distance = current_dist + distance
                if new_distance < unvisited[neighbor]:
                    unvisited[neighbor] = new_distance
                    parents[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))  # Push the neighbor with the new distance

    # Convert the visited distances to the node labels
    lengths = {nodes[i]: dist for i, dist in visited.items()}

    # Reconstruct the paths for each node
    paths = {nodes[i]: [] for i in range(num_nodes)}
    for node in range(num_nodes):
        if parents[node] is not None or node == nodes.index(start_node):
            current = node
            while current is not None:
                paths[nodes[node]].insert(0, nodes[current])
                current = parents[current]

    return lengths, paths

def vergleich_distance(random_nodes, einsatzstellen):
    all_distances = {}
    for random_node in random_nodes:
        lengths, paths = dijkstra(ungerichtet_gewichtet, random_node)
        all_distances[random_node] = (lengths, paths)
    
    zuweisungen = {random_node: [] for random_node in random_nodes}
    distance_dicts = {random_node: {} for random_node in random_nodes}
    for random_node, (lengths, paths) in all_distances.items():
        print(f"Distanzen und Pfade vom zufällig ausgewählten Knoten {random_node} zu den Einsatzstellen:")
        for einsatzstelle in einsatzstellen:
            print(f"{random_node} -> {einsatzstelle}: {lengths[einsatzstelle]} km, Pfad: {' -> '.join(paths[einsatzstelle])}")
            distance_dicts[random_node][einsatzstelle] = lengths[einsatzstelle]
    
    # Leere Matrix für die Zuweisung der Einsatzstellen
    stellen_zuweisung = np.zeros((len(nodes), len(nodes)))
    
    # Vergleiche die Distanzen und weise die kleinste Distanz zu
    for einsatzstelle in einsatzstellen:
        min_distance = float('inf')
        closest_random_node = None
        for random_node in random_nodes:
            if distance_dicts[random_node][einsatzstelle] < min_distance:
                min_distance = distance_dicts[random_node][einsatzstelle]
                closest_random_node = random_node
        
        if closest_random_node:
            zuweisungen[closest_random_node].append(einsatzstelle)
            stellen_zuweisung[nodes.index(closest_random_node)][nodes.index(einsatzstelle)] = min_distance
    
    # Entferne zufällige Knoten, die keine Zuweisung haben
    zuweisungen = {k: v for k, v in zuweisungen.items() if v}
    
    print("\nZuweisung der Einsatzstellen zu Zufalligen Knoten:")
    for random_node, zugewiesene_einsatzstellen in zuweisungen.items():
        print(f"{random_node}: {', '.join(zugewiesene_einsatzstellen)}")
    
    # Berechne die durchschnittliche Entfernung für jeden zufälligen Knoten
    for random_node in random_nodes:
        total_distance = 0
        count = 0
        if random_node in zuweisungen:
            for einsatzstelle in zuweisungen[random_node]:
                total_distance += distance_dicts[random_node][einsatzstelle]
                count += 1
            average_distance = total_distance / count if count > 0 else 0
            print(f"\nDurchschnittliche Entfernung für {random_node}: {average_distance:.2f} km")
    
    return stellen_zuweisung

def run_verpflegungspunkte():
    k = int(input("Wie viele Versorgungspunkte möchten Sie hinzufügen? (1-6): "))
    
    # Wähle k zufällige Knoten, die nicht in den Einsatzstellen enthalten sind
    remaining_nodes = [node for node in nodes if node not in einsatzstellen]
    random_nodes = random.sample(remaining_nodes, k)
    print(f"Zufällig ausgewählte Knoten: {random_nodes}")

    stellen_zuweisung = vergleich_distance(random_nodes, einsatzstellen)
