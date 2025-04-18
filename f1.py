import heapq
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from b1 import ungerichtet_gewichtet

def prim(graph, important_nodes):
    """
    Berechnet den Minimal Spanning Tree (MST) nur für die markierten Knoten.
    Der Graph wird als Adjazenzmatrix dargestellt, und nur die Kanten der markierten Knoten werden berücksichtigt.

    prim ist eine Greedy Algorithmus
    """
    n = len(graph)
    mst = []  # Liste für die Kanten des MST
    visited = [False] * n  # Knoten, die bereits im MST enthalten sind
    min_heap = []  # Min-Heap für die Prim-Algorithmen
    total_weight = 0
    prev_node = -1  # Variable, um die vorherige Kante zu speichern
    
    # Startknoten aus den wichtigen Knoten auswählen (erster Knoten in der Liste)
    start_node = important_nodes[0]
    visited[start_node] = True

    # Füge alle benachbarten Knoten zum Min-Heap hinzu, die zu den wichtigen Knoten gehören
    for neighbor in important_nodes:
        if graph[start_node][neighbor] != 0:
            heapq.heappush(min_heap, (graph[start_node][neighbor], start_node, neighbor))
    
    while min_heap:
        weight, node1, node2 = heapq.heappop(min_heap)
        
        if visited[node2]:
            continue
        
        # Markiere den Knoten als besucht
        visited[node2] = True
        mst.append((node1, node2, weight))  # Füge Kante zum MST hinzu
        total_weight += weight
        
        # Füge neue Kanten hinzu
        for neighbor in important_nodes:
            if not visited[neighbor] and graph[node2][neighbor] != 0:
                heapq.heappush(min_heap, (graph[node2][neighbor], node2, neighbor))
                
    return mst, total_weight

def visualize():
    """
    visualisiert den Graphen, wobei die Kanten des MST in rot hervorgehoben werden.
    """
    # Beispiel für ein Mapping von Knoten zu ihren Typen:
    node_types = {
        0: 'Rettungsstation',  # A
        1: 'Rettungsstation',  # B
        2: 'Rettungsstation',  # C
        3: 'Krankenhaus',      # D
        4: 'Rathaus',          # E
        5: 'Krankenhaus',      # F
        6: 'AKW',              # G
        7: 'Sonstiges',        # H
        8: 'Sonstiges',        # I
        9: 'Sonstiges'         # J
    }

    # Beispielgraph (Adjazenzmatrix)
    graph = ungerichtet_gewichtet
    # Wichtige Knoten (alle Knoten außer 'Sonstiges')
    important_nodes = [0, 1, 2, 3, 4, 5, 6]  # A=0, B=1, C=2, D=3, E=4, F=5, G=6

    # Berechnung des MST für die markierten Knoten
    mst, total_weight = prim(graph, important_nodes)

    # Ausgabe des Minimal Spanning Trees (MST)
    print("Minimal Spanning Tree (MST):")
    for edge in mst:
        print(f"{chr(edge[0] + 65)} - {chr(edge[1] + 65)} mit Gewicht {edge[2]}")

    print(f"\nGesamtkosten des MST: {total_weight}")

    # Visualisierung des Graphen mit NetworkX und Matplotlib
    G = nx.Graph()

    # Hinzufügen der Knoten
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for node in nodes:
        G.add_node(node)

    # Hinzufügen der Kanten (für alle Knoten, nicht nur die wichtigen)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if graph[i][j] != 0:
                G.add_edge(nodes[i], nodes[j], weight=graph[i][j])

    # Zeichnen des gesamten Graphen
    pos = nx.spring_layout(G)  # Layout für die Visualisierung

    plt.figure(figsize=(8, 8))

    # Farben für verschiedene Knotenarten basierend auf `node_types`
    node_colors = []
    for i in range(len(nodes)):
        node_type = node_types.get(i, 'Sonstiger')  # Standardwert 'Sonstiger'
        if node_type == 'Rettungsstation':
            node_colors.append('green')
        elif node_type == 'Krankenhaus':
            node_colors.append('red')
        elif node_type == 'Rathaus':
            node_colors.append('yellow')
        elif node_type == 'AKW':
            node_colors.append('pink')
        else:
            node_colors.append('lightblue')

    # Zeichnen der Knoten
    nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=12, font_weight='bold')

    # Kanten, die zum MST gehören, in rot zeichnen
    edges = G.edges()
    mst_edges = [(nodes[edge[0]], nodes[edge[1]]) for edge in mst]  # MST-Kanten
    edge_colors = []
    edge_labels = {}  # Für Kantenbeschriftungen

    # Iteration durch die Kanten und ihre Farben
    for u, v in edges:
        # Wenn die Kante im MST enthalten ist, färbe sie rot, andernfalls schwarz
        if (u, v) in mst_edges or (v, u) in mst_edges:
            edge_colors.append('red')
            edge_labels[(u, v)] = graph[nodes.index(u)][nodes.index(v)]  # Gewicht der Kante hinzufügen
        else:
            edge_colors.append('black')

    # Kanten zeichnen
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=2)

    # Kantenbeschriftungen (Gewicht)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Legende erstellen
    legend_elements = [
        mpatches.Patch(color='green', label='Rettungsstation'),
        mpatches.Patch(color='red', label='Krankenhaus'),
        mpatches.Patch(color='yellow', label='Rathaus'),
        mpatches.Patch(color='pink', label='AKW'),
        mpatches.Patch(color='lightblue', label='Noch nicht benannt')
    ]

    plt.legend(handles=legend_elements, loc='upper right')

    # Anzeigen der Visualisierung
    plt.title("Graph mit Minimal Spanning Tree (MST) für wichtige Knoten in Rot und Gewichtung der Kanten")
    plt.show()
