import heapq, os
from b1 import print_matrix, nodes, gerichtet_gewichtet
'''
Routenberechnung der Einsatzkräfte mit hilfe des Dijkstra Algorithmus und einer Min-Heap Datenstruktur

'''

# Gerichtet, gewichtet Graph (Adjazenzmatrix)
graph = gerichtet_gewichtet

# Dijkstra-Algorithmus zur Berechnung der kürzesten Entfernung
def dijkstra(graph, start, ziel):
    n = len(graph) #Anzahl der Knoten
    dist = [float('inf')] * n  # Start mit Unendlichkeit für alle Knoten
    dist[start] = 0  # Der Abstand zum Startknoten ist 0
    visited = [False] * n #beginn, alle Knoten unbesucht
    prev = [None] * n  # Array für Vorgänger-Knoten
    pq = [(0, start)]  # Priority Queue mit (Abstand, Knoten)
    
    while pq: #solange bis pq = 0
        current_dist, u = heapq.heappop(pq) #Tupel mit niedrigster Distanz aus PQ
        
        if visited[u]: #wenn knoten bereits besucht, fortfahren
            continue
        visited[u] = True #als besucht markieren
        
        for v in range(n): # v = Knoten, für jeden nachbarn von v  
            if graph[u][v] > 0 and not visited[v]:  # Wenn Kante existiert & Knoten nicht besucht
                new_dist = current_dist + graph[u][v] #neue distanz zu v, aktuelle u + v addierne
                if new_dist < dist[v]: # wenn new < als forherigen, bleiben wir auf diesem Knoten
                    dist[v] = new_dist
                    prev[v] = u  # Setze den Vorgänger von v auf u
                    heapq.heappush(pq, (new_dist, v)) #neue distanz mit v in PQ
    
    return dist, prev  # Rückgabe der Distanzen und Vorgänger




# Pfad von Start- zu Zielknoten rekonstruieren
def routenberechnung(prev, ziel):
    path = []
    current = ziel
    while current is not None:
        path.append(current)
        current = prev[current]
    
    path.reverse()  # Umkehren, da wir den Pfad vom Ziel zum Start rekonstruieren
    return path





# New function to run the Einsatzplanung (Dispatch Planning)
def run_einsatzplanung():
    os.system('cls' if os.name == 'nt' else 'clear')

    
    # Printet den Graphen
    print_matrix(graph, nodes)
    # Benutzerabfrage für den Start- und Zielknoten
    start_input = int(input("Standort (0-9): "))
    ziel_input = int(input("Unfallstelle (0-9): "))

    # Berechnung der kürzesten Entfernung und des Pfades
    distanz, prev = dijkstra(graph, start_input, ziel_input)

    # Ausgabe der kürzesten Entfernung
    print(f"Die kürzeste Entfernung von {chr(start_input + 65)} nach {chr(ziel_input + 65)} beträgt {distanz[ziel_input]}.")

    # Berechnung des Pfades
    path = routenberechnung(prev, ziel_input)
    print(f"Die Route ist: {' -> '.join([chr(k + 65) for k in path])}")

    # Einsatzabfrage
    antwort = input("Möchten Sie den Einsatz annehmen? (y/n): ").strip().lower()

    # Status der Einsatzkraft (verfügbar oder nicht)
    available = True

    if antwort == "y":
        available = False  # Einsatzkraft ist nun nicht mehr verfügbar
        print("Einsatzkraft hat den Einsatz angenommen.")
        
        while True:
            status = input("Geben Sie 'y' ein, wenn Sie mit dem Einsatz fertig sind: ").strip().lower()

            if status == 'y':
                available = True
                print("Einsatz abgeschlossen.")
                break
            else:
                print("Nicht abgeschlossen, bleibt unverfügbar.")
    else:
        print("Einsatzkraft hat den Einsatz abgelehnt. Sie bleiben verfügbar.")

    # Rückgabe der Verfügbarkeit
    print(f"Verfügbarkeit der Einsatzkraft: {available}")

