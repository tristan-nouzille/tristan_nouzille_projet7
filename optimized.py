import csv
import time
import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# Charger les données depuis un fichier CSV
def charger_donnees(fichier):
    actions = []
    try:
        with open(fichier, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if not {'name', 'price', 'profit'} <= set(reader.fieldnames):
                raise ValueError("Format incorrect du fichier CSV.")

            for row in reader:
                try:
                    nom = row['name'].strip()
                    cout = float(row['price'].strip())
                    benefice = float(row['profit'].strip())

                    if cout > 0 and benefice > 0:
                        actions.append((nom, cout, benefice))
                except ValueError:
                    print(f"{Fore.RED}Erreur dans le format des données pour l'action : {row.get('name', 'inconnue')}")
    except FileNotFoundError:
        print(f"{Fore.RED}Fichier introuvable : {fichier}")
    except Exception as e:
        print(f"{Fore.RED}Erreur lors du chargement de {fichier} : {e}")
    return actions

# Algorithme d'optimisation (sac à dos)
def optimiser_investissement(actions, budget_max):
    n = len(actions)
    budget_max = int(budget_max * 100)
    actions = [(nom, int(cout * 100), benefice) for nom, cout, benefice in actions]

    dp = [[0] * (budget_max + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        nom, cout, benefice = actions[i - 1]
        for b in range(budget_max + 1):
            if cout > b:
                dp[i][b] = dp[i - 1][b]
            else:
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - cout] + benefice)

    b = budget_max
    meilleure_combinaison = []
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            nom, cout, benefice = actions[i - 1]
            meilleure_combinaison.append((nom, cout / 100, benefice))
            b -= cout

    return meilleure_combinaison[::-1], dp[n][budget_max]

# Analyse d’un fichier CSV donné
def analyser_fichier(fichier, budget_max=500):
    print(f"\n📊 {Style.BRIGHT}Analyse du fichier : {Fore.CYAN}{fichier}{Style.RESET_ALL}")
    print("------------------------------------------------------------")

    debut = time.time()
    actions = charger_donnees(fichier)

    if not actions:
        print(f"{Fore.RED}Aucune action valide trouvée. Fichier ignoré.")
        return

    combinaison, profit_total = optimiser_investissement(actions, budget_max)
    cout_total = sum(a[1] for a in combinaison)
    duree = time.time() - debut

    print(f"\n✅ {Style.BRIGHT}Meilleure sélection d'actions :")
    for nom, cout, benefice in combinaison:
        print(f"- {nom} (Coût : {Fore.BLUE}{cout:.2f} €{Style.RESET_ALL}, "
              f"Bénéfice : {Fore.GREEN}{benefice:.2f} €{Style.RESET_ALL})")

    print(f"\n💰 Coût total : {Fore.RED}{cout_total:.2f} €")
    print(f"📈 Bénéfice total : {Fore.GREEN}{profit_total:.2f} €")
    print(f"⏳ Temps de calcul : {duree:.4f} secondes")
    print("------------------------------------------------------------")

# Fonction principale
def main():
    dossier = "./datasets"
    fichiers = ["dataset1_Python+P7.csv", "dataset2_Python+P7.csv"]

    for fichier in fichiers:
        chemin_complet = os.path.join(dossier, fichier)
        analyser_fichier(chemin_complet)

if __name__ == "__main__":
    main()

