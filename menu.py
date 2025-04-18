from b1 import print_matrix, nodes, ungerichtet_gewichtet, ungerichtet_ungewichtet, gerichtet_gewichtet, gerichtet_ungewichtet
import os, b2, f1, f2, f3, f4, f5

def wait_for_return_to_menu():
    input("\nDrücke Enter, um zum Hauptmenü zurückzukehren...")
    os.system('cls' if os.name == 'nt' else 'clear')
    

def show_main_menu():
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║     🌍 Planungstool für Katastrophenmanagement 🌍      ║")
    print("╠════════════════════════════════════════════════════════╣")
    print("║  b1: 🗺️  Stadtplan einlesen und ausgeben                ║")
    print("║  b2: ✏️  Stadtplan modifizieren                         ║")
    print("║--------------------------------------------------------║")
    print("║  f1: 📡 Kommunikationsinfrastruktur wiederaufbauen     ║")
    print("║  f2: 🛣️  Evakuierungsrouten planen                      ║")
    print("║  f3: 🗺️  Routenplanung für die Einsatzkräfte            ║")
    print("║  f4: 📦 Versorgung von Einsatzkräften                  ║")
    print("║  f5: 🚨 Einsatzplanung für Einsatzkräfte               ║")
    print("║--------------------------------------------------------║")
    print("║  x: ❌ EXIT                                            ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("💡 Hinweis: Wählen Sie eine Option(z.B: b1) und drücken Sie [Enter]!")


def main():
    while True:
        show_main_menu()  # Menü anzeigen

        choice = input("Auswahl eingeben: ")

        if choice == "b1":
            while True:
                print("Choose which graph to show:")
                print("1. Ungerichtet Gewichtet")
                print("2. Ungerichtet Ungewichtet")
                print("3. Gerichtet Gewichtet")
                print("4. Gerichtet Ungewichtet")
                print("x. Zurück zum Hauptmenü")
                choice_graph = input("Auswahl eingeben: ")
                if choice_graph == "1":
                    print("Adjacency matrix for Ungerichtet Gewichtet:")
                    print_matrix(ungerichtet_gewichtet, nodes)
                elif choice_graph == "2":
                    print("Adjacency matrix for ungerichtet_ungewichtet:")
                    print_matrix(ungerichtet_ungewichtet, nodes)
                elif choice_graph == "3":
                    print("Adjacency matrix for gerichtet_gewichtet:")
                    print_matrix(gerichtet_gewichtet, nodes)
                elif choice_graph == "4":
                    print("Adjacency matrix for gerichtet_ungewichtet:")
                    print_matrix(gerichtet_ungewichtet, nodes)
                elif choice_graph == "x":
                    break
                else:
                    print("Invalid choice. Please try again.")
                    print()

        elif choice == "b2":
            b2.test()

        elif choice == "f1":
            # F1: Kommunikationsinfrastruktur wiederaufbauen
            print("Berechne und visualisiere den Minimal Spanning Tree (MST)...")
            f1.visualize()  # Berechnet und visualisiert den MST automatisch
            wait_for_return_to_menu()  # Warten auf Rückkehr zum Menü

        elif choice == "f2":
            print("Running Evakuierungsrouten Planung...")
            f2.run_simulation()
            wait_for_return_to_menu()
        elif choice == "f3":
            print("Running Routenplanung für Einsatzkräfte...")
            f3.run_einsatzplanung()  # Führt die Funktion für Routenplanung aus
            wait_for_return_to_menu()  # Warten auf Rückkehr zum Menü

        elif choice == "f4":
            print("Running Versorgung von Einsatzkräften...")
            f4.run_verpflegungspunkte() # Führt die Funktion für die Versorgung aus
            wait_for_return_to_menu()  # Warten auf Rückkehr zum Menü

        elif choice == "f5":
            print("Wählen Sie das Team, dem Sie angehören:")
            print("1. Team A")
            print("2. Team B")
            team_choice = input("Enter your choice: ")
            if team_choice == "1":
                f5.plan_einsatz(team_name="Team A")  # Übergibt das Team A an F5
            elif team_choice == "2":
                f5.plan_einsatz(team_name="Team B")  # Übergibt das Team B an F5
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
                continue
            wait_for_return_to_menu()  # Warten auf Rückkehr zum Menü

        elif choice == "x":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()  # Starte das Hauptmenü



