# 🚀 Guide de Démarrage Rapide - AeroWise Chatbot Phase 1

## ⚡ Installation Express (Windows)

### 1. Ouvrir un terminal PowerShell ou CMD

```powershell
# Se placer dans le dossier du projet
cd chemin\vers\aerowise_chatbot
```

### 2. Créer un environnement virtuel

```powershell
python -m venv venv
```

### 3. Activer l'environnement virtuel

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat
```

Vous devriez voir `(venv)` apparaître au début de votre ligne de commande.

### 4. Installer les dépendances

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

⏳ Cela prendra environ 2-3 minutes.

### 5. Tester l'installation

```powershell
python main.py
```

Si tout fonctionne, vous verrez :

```
====================================================================
🦉                      AEROWISE CHATBOT                        🦉
====================================================================
Gestion intelligente de la biodiversité aéroportuaire
Phase 1 - MVP avec données mockées
====================================================================

⏳ Initialisation de l'agent...
✅ Agent initialisé avec:
   - 15 espèces
   - 20 observations
   - 8 zones
   - 10 incidents

✅ Agent prêt ! Posez vos questions (tapez 'help' pour voir des exemples)

🧑 Vous :
```

## 🎮 Utilisation

### Poser des questions

Tapez simplement votre question et appuyez sur Entrée :

```
🧑 Vous : Quels oiseaux ont été observés près de la piste 2 ce mois-ci ?

🤖 AeroWise : Dans la zone **Piste 2 (08R/26L)**, les oiseaux suivants ont été observés récemment :

- **Corneille noire** (Corvus corone)
- **Vanneau huppé** (Vanellus vanellus)

*Total : 2 espèce(s) observée(s)*
```

### Commandes spéciales

- `help` ou `?` : Afficher l'aide et des exemples
- `stats` : Voir les statistiques de la base de données
- `quit` ou `exit` : Quitter le chatbot

## 🧪 Lancer les tests

Pour vérifier que tout fonctionne correctement :

```powershell
pytest tests/ -v
```

Résultat attendu :

```
======================== test session starts =========================
collected 25 items

tests/test_agent.py::TestQueryTypeDetection::test_detect_spatial_query PASSED
tests/test_agent.py::TestQueryTypeDetection::test_detect_descriptive_query PASSED
...
======================== 25 passed in 2.5s ==========================
```

## ❓ Exemples de Questions à Tester

### 1️⃣ Requêtes Spatiales (localisation)
```
Quels oiseaux ont été observés près de la piste 2 ce mois-ci ?
```

### 2️⃣ Requêtes Descriptives (description d'espèce)
```
Donne-moi la description de l'espèce Vanneau huppé
Décris-moi la Corneille noire
```

### 3️⃣ Requêtes Analytiques (analyse/menaces)
```
Donne-moi une espèce de plante menacée par l'aéroport
Quels oiseaux ont un risque de collision élevé ?
```

### 4️⃣ Requêtes de Similarité
```
Montre-moi des observations similaires à l'observation #5
Observations comparables à #12
```

### 5️⃣ Requêtes d'Alertes
```
Y a-t-il des risques particuliers cette semaine ?
Analyse les incidents récents
```

## 🐛 Dépannage

### Erreur : "python not found"
➡️ Vérifiez que Python 3.10+ est installé : `python --version`

### Erreur lors de l'installation des dépendances
➡️ Mettez à jour pip : `python -m pip install --upgrade pip`

### L'agent ne démarre pas
➡️ Vérifiez que vous êtes dans le bon dossier : `dir` (doit afficher main.py)

### Tests échouent
➡️ Vérifiez que pytest est installé : `pip install pytest pytest-cov`

## 📊 Structure du Projet

```
aerowise_chatbot/
├── agents/              # Logique de l'agent
│   └── mock_agent.py   # Agent principal
├── data/               # Données mockées
│   ├── mock_species.json
│   ├── mock_observations.json
│   ├── mock_zones.json
│   └── mock_incidents.json
├── models/             # Modèles Pydantic
│   └── schemas.py
├── tests/              # Tests unitaires
│   └── test_agent.py
├── main.py            # Interface CLI
└── requirements.txt   # Dépendances
```

## 🎯 Prochaines Étapes

Une fois que Phase 1 fonctionne :

1. ✅ **Comprendre le code** : Ouvre `agents/mock_agent.py` et lis les commentaires
2. ✅ **Modifier les réponses** : Personnalise les réponses de l'agent
3. ✅ **Ajouter des données** : Enrichis les fichiers JSON dans `/data`
4. ⏭️ **Phase 2** : Intégration avec PostGIS (quand ton camarade aura commit)

## 💡 Astuces

- Utilise `stats` pour voir le contenu de la base
- Les données sont dans `/data` (fichiers JSON facilement modifiables)
- Le code est commenté pour faciliter la compréhension
- Tous les tests doivent passer avant de passer à Phase 2

## 🆘 Besoin d'aide ?

- Consulte `README.md` pour plus de détails
- Lis le document `AeroWise_Chatbot_Specification.docx`
- Vérifie les tests dans `tests/test_agent.py` pour des exemples d'utilisation

---

**Dernière mise à jour** : Février 2025  
**Version** : Phase 1 MVP
