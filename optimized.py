import csv
import time
import colorama
from colorama import Fore, Style

colorama.init()

# Charger les données du fichier CSV
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

                    benefice_pourcent = row['Bénéfice (après 2 ans)'].strip()
                    if benefice_pourcent.endswith('%'):
                        benefice_pourcent = float(benefice_pourcent.replace('%', ''))
                    else:
                        benefice_pourcent = float(benefice_pourcent)

                    benefice = cout * (benefice_pourcent / 100)

                    if cout > 0 and benefice > 0:  # Ne garder que les actions rentables
                        actions.append((nom, cout, benefice))
                except ValueError:
                    print(f"{Fore.RED}Erreur dans le format des données pour l'action {row['Actions #']}{Style.RESET_ALL}")

    except FileNotFoundError:
        print(f"{Fore.RED}Erreur : Fichier {fichier} introuvable !{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Erreur : {e}{Style.RESET_ALL}")

    return actions

# Algorithme du sac à dos (Optimisation dynamique)
def optimiser_investissement(actions, budget_max):
    n = len(actions)
    budget_max = int(budget_max * 100)  # Conversion pour éviter les erreurs de float
    actions = [(nom, int(cout * 100), benefice) for nom, cout, benefice in actions]

    # Table de programmation dynamique
    dp = [[0] * (budget_max + 1) for _ in range(n + 1)]

    # Remplissage du tableau
    for i in range(1, n + 1):
        nom, cout, benefice = actions[i - 1]
        for b in range(budget_max + 1):
            if cout > b:
                dp[i][b] = dp[i - 1][b]
            else:
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - cout] + benefice)

    # Reconstruction de la meilleure sélection
    b = budget_max
    meilleure_combinaison = []
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:  # L'action a été sélectionnée
            nom, cout, benefice = actions[i - 1]
            meilleure_combinaison.append((nom, cout / 100, benefice))
            b -= cout

    return meilleure_combinaison, dp[n][budget_max]

# Fonction principale
def main():
    fichier_actions = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"  
    budget_max = 500  

    debut = time.time()

    actions = charger_donnees(fichier_actions)

    if not actions:
        print(f"{Fore.RED}Aucune action valide trouvée. Vérifiez le fichier.{Style.RESET_ALL}")
        return

    meilleure_combinaison, meilleur_benefice = optimiser_investissement(actions, budget_max)

    fin = time.time()
    temps_execution = fin - debut

    # Affichage des résultats
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
