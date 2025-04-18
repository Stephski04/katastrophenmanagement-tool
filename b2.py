#B2: Stadtplan modifizieren
import os 
import b1
from b1 import print_matrix, nodes, ungerichtet_gewichtet, ungerichtet_ungewichtet, gerichtet_gewichtet, gerichtet_ungewichtet
#funtion to add a new node 
def add_node(graph, node_name):
    nodes.append(str(node_name))
    for i in range(len(graph)):
        graph[i].append(0)
    graph.append([0] * (len(graph) + 1))
    graph[-1][-1] = 0
    return graph

#function to add a new edge 
def add_edge(graph, node1, node2, weight):
    graph[node1][node2] = weight
    if graph is not gerichtet_gewichtet and graph is not gerichtet_ungewichtet:
        graph[node2][node1] = weight
    return

#function to remove a node 
def remove_node(graph, node):
    nodes.pop(node)
    graph.pop(node)
    for i in range(len(graph)):
        graph[i].pop(node)
    return graph


def test():
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        print()
        print("====================================================")
        print("Wählen Sie den zu modifizierenden Graphen:")
        print("1. Ungerichtet Gewichtet")
        print("2. Ungerichtet Ungewichtet")
        print("3. Gerichtet Gewichtet")
        print("4. Gerichtet Ungewichtet")
        print("x. Zurück zum Menü")
        print("====================================================")

        choice_graph = input("Graph auswählen: ")
        if choice_graph == "1":
            graph = ungerichtet_gewichtet
        elif choice_graph == "2":
            graph = ungerichtet_ungewichtet
        elif choice_graph == "3":
            graph = gerichtet_gewichtet
        elif choice_graph == "4":
            graph = gerichtet_ungewichtet
        elif choice_graph == "x":
            print("Zurück zum Hauptmenü...")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
            continue

        while True:
            print()
            print("====================================================")
            print("Was möchten Sie am ausgewählten Graphen modifizieren?")
            print("0. Graph anzeigen")
            print("1. Knoten hinzufügen")
            print("2. Kante hinzufügen")
            print("3. Knoten entfernen")
            print("x. Zurück zur Graphenauswahl")
            print("====================================================")

            choice_b2 = input("Modifikation auswählen: ")
            if choice_b2 == "0":
                os.system('cls' if os.name == 'nt' else 'clear')

                print_matrix(graph, nodes)
            elif choice_b2 == "1":
                print("Knoten hinzufügen")
                node_name = input("Name des Knotens: ")
                add_node(graph, node_name)
            elif choice_b2 == "2":
                print("Kante hinzufügen")
                node1 = int(input("Von Knoten: "))
                node2 = int(input("Zu Knoten: "))
                weight = int(input("Gewicht der Kante: "))
                add_edge(graph, node1, node2, weight)
            elif choice_b2 == "3":
                print("Knoten entfernen (0-9)")
                node = int(input("Knoten zum Entfernen: "))
                remove_node(graph, node)

            elif choice_b2 == "x":
                print("Zurück zur Graphenauswahl...")
                break
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")