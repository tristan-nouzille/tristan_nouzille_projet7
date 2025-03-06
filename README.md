### tristan_nouzille_projet7

## Installation

1. Clonez le dépôt :

 ```
 git clone https://github.com/tristan-nouzille/tristan_nouzille_projet7
 ```
 Ensuite accédez au dossier en tapant cette ligne :

  ```
  cd tristan_nouzille_projet7
  ```
2. Créez un environnement virtuel (optionnel mais recommandé) :

# Sur macOS et Linux
a. installer virtualenv:

 ```
 python3 -m pip install virtualenv
 ```
b. créez votre dossier d'environnement virtuel:

 ```
 python3 -m virtualenv venv
 ```
c. Activez votre environnement avec :

  ```
  source venv/bin/activate 
  ```
  une fois effectuer, votre terminal s'affichera comme ceci :

  ```
  (env)
  NOM_de_votre_pc-PC ~/nom_de_votre_dossier/tristan_nouzille_projet4
  ```

# Sur Windows
 
a. installer virtualenv:

 ```
 pip install virtualenv
 ```
b. créez votre dossier d'environnement virtuel:

 ```
 python -m venv env
 ```
c. Activez votre environnement avec :

  ```
  source env\Scripts\activate  
  ```
 Une fois effectuer, votre terminal s'affichera comme ceci :
  ```
  (env)
  NOM_de_votre_pc-PC ~/nom_de_votre_dossier/tristan_nouzille_projet4
  ```
## Pseudocode 

Début

  # Entrées : 
  # - liste_actions : liste contenant les actions (coût, profit)
  # - budget_max : budget disponible

  n ← nombre d'actions
  Créer un tableau dp de taille (n+1) × (budget_max+1) initialisé à 0

  # Remplissage du tableau dp
  Pour i allant de 1 à n :
    Pour j allant de 0 à budget_max :
      Si coût de l'action[i] ≤ j :
        # On choisit le maximum entre :
        # - Ne pas prendre l'action (dp[i-1][j])
        # - Prendre l'action (profit + meilleure valeur possible pour le budget restant)
        dp[i][j] ← max(dp[i-1][j], profit[i] + dp[i-1][j - coût[i]])
      Sinon :
        # On ne peut pas prendre l'action
        dp[i][j] ← dp[i-1][j]

  # Reconstruction de la solution optimale
  Meilleure_combinaison ← []
  i ← n, j ← budget_max

  Tant que i > 0 et j > 0 :
    Si dp[i][j] ≠ dp[i-1][j] :
      Ajouter l'action[i] à Meilleure_combinaison
      j ← j - coût[i]
    i ← i - 1

  # Affichage des résultats
  Afficher "Meilleure combinaison d'actions :", Meilleure_combinaison
  Afficher "Bénéfice total :", dp[n][budget_max]

Fin

