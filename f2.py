# Import der Knotenliste und der gerichteten Gewichtsmatrix aus dem Modul b1
from b1 import nodes, gerichtet_gewichtet

# Konfiguration der Sammelstellen mit ihren Kapazitäten
sammelstellen = {
    "C": 500, 
    "F": 300
}

# Konfiguration der Notlager mit ihren Aufnahmekapazitäten
notlager = {
    "I": 700,  
    "J": 500,  
    "H": 100   
}

# Transportkonfiguration
busse = 20             # Gesamtanzahl verfügbarer Busse
kapazitaet_bus = 50    # Maximale Kapazität pro Bus

# Aktualisierte Straßenmatrix (Adjazenzmatrix) mit aktuellen Kapazitäten
# Die Matrix repräsentiert die verbundenen Knoten und ihre Transportkapazitäten
aktualisierter_stadtplan = [
    # A   B    C   D   E     F   G   H     I   J
    [0,  100, 0,  0,  200,  0,  0,  800, 0,  250],  # A
    [0,  0,   180,0,  200,  250, 0,  0,   0,  300],  # B
    [0,  180, 0,  120,200,  0,  300,250, 0,  0  ],  # C
    [100,0,   120,0,  100,  0,  0,  0,   0,  0  ],  # D
    [200,200, 200,100,0,   300, 0,  0,   0,  0  ],  # E
    [0,  250, 0,  0,  300,  0,  0,  0,   0,  400],  # F
    [0,  0,   300,0,  0,    0,  0,  600,500,0  ],  # G
    [800,0,   250,0,  0,    0,  600,0,   0,  0  ],  # H
    [0,  0,   0,  0,  0,    0,  500,0,   0,  0  ],  # I
    [250,300, 0,  0,  0,   400, 0,  0,   0,  0  ],  # J
]

def vergleichen_und_klassifizieren(gerichtet_gewichtet, aktualisierter_stadtplan):

    einbahnstrassen = []
    unpassierbare_strassen = []

    # Durchlaufen aller Knotenpaare in der Matrix
    for i in range(len(gerichtet_gewichtet)):
        for j in range(len(gerichtet_gewichtet[i])):
            if i != j:  # Diagonalelemente ignorieren
                # Fall 1: Straße existierte ursprünglich, ist jetzt unpassierbar
                if gerichtet_gewichtet[i][j] != 0 and aktualisierter_stadtplan[i][j] == 0:
                    unpassierbare_strassen.append((nodes[i], nodes[j]))
                
                # Fall 2: Einbahnstraße erkannt (nur in eine Richtung passierbar)
                elif gerichtet_gewichtet[i][j] != 0 and aktualisierter_stadtplan[i][j] != 0 and aktualisierter_stadtplan[j][i] == 0:
                    einbahnstrassen.append((nodes[i], nodes[j]))

    return einbahnstrassen, unpassierbare_strassen

def max_flow(graph, source, sink):

    def bfs(graph, source, sink, parent):
        """
        Breadth-First Search zur Findung von augmentierenden Pfaden.
        """
        visited = [False] * len(graph)
        queue = [source]
        visited[source] = True
        
        while queue:
            u = queue.pop(0)  # Warteschlange nach FIFO-Prinzip
            # Untersuche alle Nachbarknoten
            for ind, val in enumerate(graph[u]):
                # Wenn Knoten nicht besucht und positive Kapazität
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u  # Merke Parent-Knoten für Pfadrekonstruktion
        return visited[sink]

    parent = [-1] * len(graph)  # Parent-Array für Pfadverfolgung
    max_flow_value = 0          # Gesamtfluss
    all_paths = []              # Liste aller genutzten Pfade

    # Hauptschleife: Solange augmentierende Pfade existieren
    while bfs(graph, source, sink, parent):
        # Pfad von Senke zur Quelle rekonstruieren
        path = []
        v = sink
        while v != source:
            path.append(nodes[v])  # Füge Knotennamen hinzu
            v = parent[v]
        path.append(nodes[source])
        path.reverse()  # Korrekte Reihenfolge von Quelle zu Senke

        # Finde den minimalen Fluss im aktuellen Pfad
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        # Aktualisiere Gesamtfluss und Graph
        max_flow_value += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow  # Reduziere Restkapazität
            graph[v][u] += path_flow  # Erhöhe Rückflusskapazität
            v = parent[v]
        
        all_paths.append((path_flow, path))

    # Finde den Pfad mit dem größten Einzelfluss
    if all_paths:
        best_path = max(all_paths, key=lambda x: x[0])[1]
    else:
        best_path = []

    return max_flow_value, best_path

def alle_maximalen_fluesse(aktualisierter_stadtplan, nodes, sammelstellen, notlager):
    """
    Berechnet den maximalen Fluss für alle Kombinationen von Sammelstellen und Notlagern.
    """
    for sammelstelle in sammelstellen:
        for notlager_name in notlager:
            # Bestimme Knotenindizes
            source = nodes.index(sammelstelle)
            sink = nodes.index(notlager_name)
            
            # Kopiere den Graphen für jede Berechnung (wird modifiziert)
            graph_copy = [row[:] for row in aktualisierter_stadtplan]
            
            # Berechne maximalen Fluss
            max_flow_value, path = max_flow(graph_copy, source, sink)
            
            # Ausgabe der Ergebnisse
            print(f"Maximaler Fluss von {sammelstelle} nach {notlager_name}: {max_flow_value}")
            print(f"Pfad: {' -> '.join(path)}")

def check_capacity(sammelstellen, notlager):
    """
    Überprüft ob die Notlagerkapazitäten für alle Personen ausreichen.
    """
    total_people = sum(sammelstellen.values())
    total_capacity = sum(notlager.values())
    return total_people <= total_capacity

def check_bus_capacity(sammelstellen, busse, kapazitaet_bus):
    """
    Überprüft ob die Buskapazitäten für alle Personen ausreichen.
    """
    total_people = sum(sammelstellen.values())
    total_capacity = busse * kapazitaet_bus
    return total_people <= total_capacity

def allocate_buses():
    """
    Verteilt Busse optimal auf die Evakuierungsrouten unter Berücksichtigung:
    - Maximaler Fluss pro Route
    - Verfügbare Busse
    - Restkapazitäten der Notlager
    """
    total_people_transported = 0
    bus_allocation = []
    available_buses = busse
    available_capacity = notlager.copy()  # Kopie um Original nicht zu verändern

    for sammelstelle in sammelstellen:
        people_remaining = sammelstellen[sammelstelle]
        
        # Verteile Personen solange noch welche übrig sind und Busse verfügbar
        while people_remaining > 0 and available_buses > 0:
            best_flow = 0
            best_path = []
            best_notlager = ""
            
            # Finde das beste Notlager für aktuelle Sammelstelle
            for notlager_name in available_capacity:
                if available_capacity[notlager_name] <= 0:
                    continue  # Überspringe volle Notlager
                
                source = nodes.index(sammelstelle)
                sink = nodes.index(notlager_name)
                graph_copy = [row[:] for row in aktualisierter_stadtplan]
                max_flow_value, path = max_flow(graph_copy, source, sink)
                
                if max_flow_value > best_flow:
                    best_flow = max_flow_value
                    best_path = path
                    best_notlager = notlager_name

            if best_flow == 0:
                print(f"Kein Pfad gefunden für {sammelstelle}.")
                break

            # Berechne benötigte Busse
            people_to_transport = min(
                people_remaining, 
                best_flow, 
                available_capacity[best_notlager]
            )
            
            # Aufrunden bei der Busberechnung
            buses_needed = (people_to_transport + kapazitaet_bus - 1) // kapazitaet_bus
            
            # Anpassung falls nicht genug Busse vorhanden
            if buses_needed > available_buses:
                people_to_transport = available_buses * kapazitaet_bus
                buses_needed = available_buses

            # Aktualisiere Tracking-Variablen
            bus_allocation.append((
                sammelstelle, 
                best_notlager, 
                people_to_transport, 
                buses_needed
            ))
            total_people_transported += people_to_transport
            available_buses -= buses_needed
            people_remaining -= people_to_transport
            available_capacity[best_notlager] -= people_to_transport

            if available_capacity[best_notlager] <= 0:
                print(f"Notlager {best_notlager} hat keine Kapazität mehr.")

    # Ausgabe der Ergebnisse
    print("\nBuszuweisungen:")
    for allocation in bus_allocation:
        sammelstelle, notlager_name, people, buses = allocation
        print(f"{buses} Busse von {sammelstelle} nach {notlager_name} für {people} Personen")

    print(f"\nTotal transportierte Personen: {total_people_transported}")
    
    # Finale Kapazitätsüberprüfung
    if total_people_transported >= sum(sammelstellen.values()):
        print("Es gibt genug Busse für alle Personen.")
    else:
        print("Es gibt nicht genug Busse für alle Personen.\nWeitere Infrastruktur wird benötigt!")

def run_simulation():
    """
    Hauptfunktion für die interaktive Simulation mit Konsolenmenü.
    """
    while True:
        print("════════════════════════════════════════════════════════")
        print("\nEvakuierungsrouten planen\n")
        print("1. Kapazität der Sammelstellen, Notlager und Busse anzeigen")
        print("2. Einbahnstraßen und Unpassierbare Straßen anzeigen")
        print("3. Maximalen Fluss berechnen")
        print("4. Evakuierungsrouten planen")
        print("x. Beenden")
        
        choice = input("Wählen Sie eine Option: ")

        if choice == '1':
            # Option 1: Zeige Kapazitätsinformationen
            print("Sammelstellen:")
            for sammelstelle, kapazitaet in sammelstellen.items():
                print(f"{sammelstelle}: {kapazitaet} Personen")
            print("\nNotlager:")
            for notlager_name, kapazitaet in notlager.items():
                print(f"{notlager_name}: {kapazitaet} Personen")
            print(f"\nTotale Buskapazität: {busse * kapazitaet_bus} Personen")

        elif choice == '2':
            # Option 2: Zeige Straßenänderungen
            einbahn, unpassierbar = vergleichen_und_klassifizieren(
                gerichtet_gewichtet, 
                aktualisierter_stadtplan
            )
            print("Einbahnstraßen:")
            for strasse in einbahn:
                print(f"{strasse[0]} -> {strasse[1]}")
            print("\nUnpassierbare Straßen:")
            for strasse in unpassierbar:
                print(f"{strasse[0]} -> {strasse[1]}")

        elif choice == '3':
            # Option 3: Berechne alle maximalen Flüsse
            alle_maximalen_fluesse(
                aktualisierter_stadtplan, 
                nodes, 
                sammelstellen, 
                notlager
            )

        elif choice == '4':
            # Option 4: Starte Evakuierungsplanung
            if check_capacity(sammelstellen, notlager):
                print("\nKapazitäten ausreichend. Starte Evakuierung...")
                allocate_buses()
            else:
                print("Fehler: Notlagerkapazitäten unzureichend!")
            break

        elif choice.lower() == 'x':
            # Beenden der Simulation
            print("Simulation wird beendet.")
            break

        else:
            print("Ungültige Eingabe. Bitte versuchen Sie es erneut.")
