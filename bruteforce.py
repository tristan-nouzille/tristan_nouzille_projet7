import csv
import time
import colorama
from colorama import Fore, Style

# Initialisation colorama (nécessaire sous Windows)
colorama.init()

# Fonction pour charger les données du fichier CSV avec gestion des erreurs
def charger_donnees(fichier):
    actions = []
    try:
        with open(fichier, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if not {'Actions #', 'Coût par action (en euros)', 'Bénéfice (après 2 ans)'} <= set(reader.fieldnames):
                raise ValueError("Format incorrect du fichier CSV.")

            for row in reader:
                try:
                    nom = row['Actions #'].strip()
                    cout = float(row['Coût par action (en euros)'].strip())

                    # Vérification et conversion du bénéfice
                    benefice_pourcent = row['Bénéfice (après 2 ans)'].strip()
                    if benefice_pourcent.endswith('%'):
                        benefice_pourcent = float(benefice_pourcent.replace('%', ''))
                    else:
                        benefice_pourcent = float(benefice_pourcent)  # Cas où le `%` est absent

                    benefice = cout * (benefice_pourcent / 100)

                    if cout > 0 and benefice > 0:
                        actions.append((nom, cout, benefice))
                except ValueError:
                    print(f"{Fore.RED}Erreur dans le format des données pour l'action {row['Actions #']}{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}Erreur : Fichier {fichier} introuvable !{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Erreur : {e}{Style.RESET_ALL}")

    return actions

# Génération des combinaisons (Brute Force)
def generer_combinaisons(actions, index=0, combinaison_actuelle=None):
    if combinaison_actuelle is None:
        combinaison_actuelle = []
    
    if index == len(actions):
        yield combinaison_actuelle
        return
    
    # Inclure l'action actuelle dans la combinaison
    yield from generer_combinaisons(actions, index + 1, combinaison_actuelle + [actions[index]])
    
    # Ne pas inclure l'action actuelle dans la combinaison
    yield from generer_combinaisons(actions, index + 1, combinaison_actuelle)

# Trouver la meilleure combinaison d'actions
def trouver_meilleure_combinaison(actions, budget_max):
    meilleure_combinaison = []
    meilleur_benefice = 0

    for combinaison in generer_combinaisons(actions):
        cout_total = sum(action[1] for action in combinaison)
        benefice_total = sum(action[2] for action in combinaison)

        if cout_total <= budget_max and benefice_total > meilleur_benefice:
            meilleure_combinaison = combinaison
            meilleur_benefice = benefice_total

    return meilleure_combinaison, meilleur_benefice

# Fonction principale
def main():
    fichier_actions = "test.csv"  # Remplacer par le fichier réel
    budget_max = 500  # Budget maximum (peut être rendu dynamique)

    # Mesurer le temps de début
    debut = time.time()

    # Charger les données
    actions = charger_donnees(fichier_actions)

    if not actions:
        print(f"{Fore.RED}Aucune action valide trouvée. Vérifiez le fichier.{Style.RESET_ALL}")
        return

    # Trouver la meilleure combinaison
    meilleure_combinaison, meilleur_benefice = trouver_meilleure_combinaison(actions, budget_max)

    # Mesurer le temps de fin
    fin = time.time()
    temps_execution = fin - debut

    # Afficher les résultats avec les couleurs :
    print("\n📈 Meilleure sélection d'actions à acheter :")
    for action in meilleure_combinaison:
        print(f"- {action[0]} (Coût : {Fore.BLUE}{action[1]:.2f} €{Style.RESET_ALL}, "
              f"Bénéfice : {Fore.GREEN}{action[2]:.2f} €{Style.RESET_ALL})")
    
    cout_total = sum(action[1] for action in meilleure_combinaison)
    print(f"\n💰 Coût total : {Fore.RED}{cout_total:.2f} €{Style.RESET_ALL}")
    print(f"📊 Bénéfice total : {Fore.GREEN}{meilleur_benefice:.2f} €{Style.RESET_ALL}")
    print(f"\n⏳ Temps d'exécution : {temps_execution:.4f} secondes")

if __name__ == "__main__":
    main()



