import csv
from itertools import combinations

# Fonction pour charger les données du fichier CSV
def charger_donnees(fichier):
    actions = []
    with open(fichier, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            nom = row['Actions']
            cout = float(row['Coût par action (en euros)'])
            benefice_pourcent = float(row['Bénéfice (après 2 ans)'])
            # Calculer le bénéfice en euros
            benefice = cout * (benefice_pourcent / 100)
            actions.append((nom, cout, benefice))
    return actions

# Fonction pour trouver la meilleure combinaison d'actions
def trouver_meilleure_combinaison(actions, budget_max):
    meilleure_combinaison = []
    meilleur_benefice = 0

    # Générer toutes les combinaisons possibles
    for r in range(1, len(actions) + 1):
        for combinaison in combinations(actions, r):
            cout_total = sum(action[1] for action in combinaison)
            benefice_total = sum(action[2] for action in combinaison)
            
            # Vérifier si la combinaison respecte le budget
            if cout_total <= budget_max and benefice_total > meilleur_benefice:
                meilleure_combinaison = combinaison
                meilleur_benefice = benefice_total

    return meilleure_combinaison, meilleur_benefice

# Fonction principale
def main():
    fichier_actions = "Liste+d'actions+-+P7+Python+-+Feuille+1.csv"  # Remplacer par le nom réel du fichier
    budget_max = 500  # Budget maximum en euros

    # Charger les données
    actions = charger_donnees(fichier_actions)

    # Trouver la meilleure combinaison
    meilleure_combinaison, meilleur_benefice = trouver_meilleure_combinaison(actions, budget_max)

    # Afficher les résultats
    print("Actions à acheter :")
    for action in meilleure_combinaison:
        print(f"- {action[0]} (Coût : {action[1]:.2f} €, Bénéfice : {action[2]:.2f} €)")
    print(f"\nCoût total : {sum(action[1] for action in meilleure_combinaison):.2f} €")
    print(f"Bénéfice total : {meilleur_benefice:.2f} €")

if __name__ == "__main__":
    main()
