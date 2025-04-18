'''
 Einsatzplanung für Notfälle 
 bei dem Teams von Einsatzkräften (z.B. Feuerwehr, Rettung) bestimmten Einsatzstellen (z.B. Unfallorte oder Schäden) zugeordnet werden.
 Dabei wird geprüft, ob die benötigten Fähigkeiten und Ressourcen für jede Einsatzstelle vorhanden sind. 
'''

class Einsatzkraft:
    def __init__(self, name, faehigkeiten, ressourcen, standort):
        self.name = name
        self.faehigkeiten = faehigkeiten
        self.ressourcen = ressourcen
        self.standort = standort  # Standort auf dem Graphen
        self.verfuegbar = True

    def __repr__(self):
        return f"{self.name} (Fähigkeiten: {', '.join(self.faehigkeiten)}, Ressourcen: {', '.join(self.ressourcen)}, Standort: {self.standort}, Verfügbar: {self.verfuegbar})"


class Team:
    def __init__(self, name, einsatzkraefte):
        self.name = name
        self.einsatzkraefte = einsatzkraefte  # Eine Liste von Einsatzkräften im Team
        self.verfuegbar = True

    def __repr__(self):
        return f"Team {self.name} mit {len(self.einsatzkraefte)} Einsatzkräften, Verfügbar: {self.verfuegbar}"


class Einsatzstelle:
    def __init__(self, name, benoetigte_faehigkeiten, benoetigte_ressourcen, standort):
        self.name = name
        self.benoetigte_faehigkeiten = benoetigte_faehigkeiten
        self.benoetigte_ressourcen = benoetigte_ressourcen
        self.standort = standort  # Standort der Einsatzstelle

    def __repr__(self):
        return f"{self.name} (Benötigte Fähigkeiten: {', '.join(self.benoetigte_faehigkeiten)}, Ressourcen: {', '.join(self.benoetigte_ressourcen)}, Standort: {self.standort})"


# Funktion zum Abrufen von Teams und Einsatzstellen
def get_teams_and_einsatzstellen():
    # Beispiel-Einsatzkräfte für Team A
    einsatzkraefte1 = [
        Einsatzkraft("Kraft1-1", ["Radlader", "Motorsäge"], ["Radlader"], 0),
        Einsatzkraft("Kraft2-1", ["Pumpe", "Motorsäge"], ["Pumpe"], 0),
        Einsatzkraft("Kraft3-1", ["Radlader", "Motorsäge"], ["Radlader", "Motorsäge"], 0),
    ]
    # Beispiel-Einsatzkräfte für Team B
    einsatzkraefte2 = [
        Einsatzkraft("Kraft1-2", ["Radlader"], ["Radlader"], 3),
        Einsatzkraft("Kraft2-2", ["Motorsäge"], ["Motorsäge"], 3),
        Einsatzkraft("Kraft3-2", ["Radlader", "Motorsäge"], ["Radlader"], 3),
    ]
    
    # Teams erstellen
    teams = [
        Team("Team A", einsatzkraefte1),
        Team("Team B", einsatzkraefte2)
    ]
    
    # Beispiel-Einsatzstellen
    einsatzstellen = [
        Einsatzstelle("Straßensperre durch Steinschlag", ["Radlader"], ["Radlader"], 1),
        Einsatzstelle("Rohrbruch", ["Motorsäge", "Pumpe"], ["Pumpe"], 8),
        Einsatzstelle("Straßensperre durch Baum", ["Radlader", "Motorsäge"], ["Radlader"], 9),
    ]
    
    return teams, einsatzstellen


# Planungslogik für die Zuordnung der Teams zu den Einsatzstellen
def plan_einsatz(team_name=None):
    # Hole die Teams und Einsatzstellen
    teams, einsatzstellen = get_teams_and_einsatzstellen()

    # Wenn ein Team angegeben ist, filtere es
    if team_name:
        teams = [team for team in teams if team.name == team_name]
        if not teams:
            print(f"Kein Team mit dem Namen '{team_name}' gefunden.")
            return
        teams = teams[0:1]  # Wir verwenden nur das angegebene Team
    
    zugeordnete_einsatzstellen = {}

    # Versuche, Teams den Einsatzstellen zuzuordnen
    for einsatzstelle in einsatzstellen:
        passende_teams = []

        # Überprüfe jedes Team
        for team in teams:
            # Überprüfe, ob alle Fähigkeiten und Ressourcen des Teams mit den Anforderungen der Einsatzstelle übereinstimmen
            alle_anforderungen_erfuellt = all(
                faehigkeit in [faehigkeit for kraft in team.einsatzkraefte for faehigkeit in kraft.faehigkeiten]
                for faehigkeit in einsatzstelle.benoetigte_faehigkeiten
            ) and all(
                ressource in [ressource for kraft in team.einsatzkraefte for ressource in kraft.ressourcen]
                for ressource in einsatzstelle.benoetigte_ressourcen
            )
            
            # Falls alle Anforderungen erfüllt sind und das Team noch verfügbar ist
            if alle_anforderungen_erfuellt and team.verfuegbar:
                passende_teams.append(team)

        # Wenn ein passendes Team gefunden wird, ordne es zu und mache das Team und seine Einsatzkräfte unverfügbar
        if passende_teams:
            team = passende_teams[0]  # Wir nehmen das erste passende Team (wenn mehrere vorhanden sind)
            zugeordnete_einsatzstellen[einsatzstelle.name] = team.name

            # Setze das Team auf nicht verfügbar
            team.verfuegbar = False

            # Setze alle Einsatzkräfte des Teams auf nicht verfügbar
            for kraft in team.einsatzkraefte:
                kraft.verfuegbar = False

    # Ausgabe der Team-Zuweisungen (nur ein Team pro Einsatzstelle)
    for einsatzstelle_name, team_name in zugeordnete_einsatzstellen.items():
        print(f"Einsatzstelle {einsatzstelle_name} hat folgendes Team zugeordnet: {team_name}")
    
    # Ausgabe der Verfügbarkeit von Teams
    for team in teams:
        print(f"{team.name} Verfügbarkeit: {team.verfuegbar}")


