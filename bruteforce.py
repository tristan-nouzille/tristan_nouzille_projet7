import csv
import os
import time
import pandas as pd
from colorama import init, Fore, Style

init(autoreset=True)

def charger_donnees(nom_fichier):
    donnees = []
    with open(nom_fichier, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        colonnes_possibles = [
            {'Actions #', 'Coût par action (en euros)', 'Bénéfice (après 2 ans)'},
            {'name', 'price', 'profit'}
        ]

        if not any(possibles <= set(reader.fieldnames) for possibles in colonnes_possibles):
            raise ValueError(f"Format incorrect du fichier CSV. Colonnes trouvées : {reader.fieldnames}")

        if {'name', 'price', 'profit'} <= set(reader.fieldnames):
            col_nom = 'name'
            col_cout = 'price'
            col_benefice = 'profit'
        else:
            col_nom = 'Actions #'
            col_cout = 'Coût par action (en euros)'
            col_benefice = 'Bénéfice (après 2 ans)'

        for row in reader:
            try:
                nom = row[col_nom].strip()
                cout = float(row[col_cout].strip())
                benefice_val = row[col_benefice].strip()
                benefice = float(benefice_val.replace('%', '')) * cout / 100 if '%' in benefice_val else float(benefice_val)
                if cout > 0 and benefice > 0:
                    donnees.append((nom, cout, benefice))
            except (ValueError, KeyError):
                continue
    return donnees

def bruteforce(actions, budget):
    n = len(actions)
    meilleur_combinaison = []
    meilleur_benefice = 0.0
    meilleur_cout = 0.0

    for i in range(1, 2 ** n):
        combinaison = []
        cout_total = 0.0
        benefice_total = 0.0
        for j in range(n):
            if (i >> j) & 1:
                action = actions[j]
                cout_total += action[1]
                benefice_total += action[2]
                combinaison.append(action)
        if cout_total <= budget and benefice_total > meilleur_benefice:
            meilleur_combinaison = combinaison
            meilleur_benefice = benefice_total
            meilleur_cout = cout_total
    return meilleur_combinaison, meilleur_cout, meilleur_benefice

def explorer_csv(fichier):
    try:
        df = pd.read_csv(fichier)
        print(f"{Fore.CYAN}📊 Analyse exploratoire du fichier : {fichier}{Style.RESET_ALL}")
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
        print(f"{Fore.MAGENTA}Nombre total de lignes : {len(df)}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Colonnes : {list(df.columns)}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Résumé statistique :{Style.RESET_ALL}")
        print(Fore.GREEN + df.describe().to_string() + Style.RESET_ALL)
        print(f"\n{Fore.CYAN}Valeurs manquantes :{Style.RESET_ALL}")
        print(Fore.RED + df.isnull().sum().to_string() + Style.RESET_ALL)
        print(Fore.YELLOW + "-" * 60 + Style.RESET_ALL)
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de l'analyse exploratoire : {e}{Style.RESET_ALL}")

def main():
    dossier_datasets = "./datasets"
    fichiers_csv = [f for f in os.listdir(dossier_datasets) if f.endswith('.csv')]
    budget = 500

    for fichier in fichiers_csv:
        chemin_fichier = os.path.join(dossier_datasets, fichier)
        explorer_csv(chemin_fichier)

        try:
            actions = charger_donnees(chemin_fichier)
        except ValueError as e:
            print(f"{Fore.RED}Erreur : {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Aucune action valide pour {fichier}.{Style.RESET_ALL}\n")
            continue

        if not actions:
            print(f"{Fore.YELLOW}Aucune action valide pour {fichier}.{Style.RESET_ALL}\n")
            continue

        print(f"\n{Fore.BLUE}🔍 Lancement du bruteforce pour : {fichier}{Style.RESET_ALL}")
        debut = time.time()
        resultats, cout_total, benefice_total = bruteforce(actions, budget)
        fin = time.time()

        print(f"\n{Fore.GREEN}✅ Meilleure combinaison trouvée :{Style.RESET_ALL}")
        for nom, cout, benefice in resultats:
            print(f"{nom} - Coût: {cout:.2f}€, Bénéfice: {benefice:.2f}€")

        print(f"\n{Fore.GREEN}💰 Coût total : {cout_total:.2f}€{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📈 Bénéfice total : {benefice_total:.2f}€{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⏱ Temps d'exécution : {fin - debut:.2f} secondes{Style.RESET_ALL}")
        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

if __name__ == "__main__":
    main()




