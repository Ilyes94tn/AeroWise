# 🦉 AeroWise Chatbot - Phase 1 MVP

**Chatbot intelligent pour la gestion de la biodiversité aéroportuaire**

## 📁 Structure du Projet

```
aerowise_chatbot/
├── agents/              # Agents IA (Agno)
│   ├── __init__.py
│   ├── base_agent.py   # Agent de base
│   └── mock_agent.py   # Agent avec données mockées (Phase 1)
├── data/               # Données simulées
│   ├── mock_observations.json
│   ├── mock_species.json
│   └── mock_zones.json
├── models/             # Modèles de données (Pydantic)
│   ├── __init__.py
│   └── schemas.py
├── utils/              # Fonctions utilitaires
│   ├── __init__.py
│   └── helpers.py
├── tests/              # Tests unitaires
│   ├── __init__.py
│   └── test_agent.py
├── main.py            # Point d'entrée principal
├── requirements.txt   # Dépendances Python
├── .env.example       # Exemple de configuration
└── README.md          # Ce fichier
```

## 🎯 Objectif Phase 1

Créer un chatbot MVP qui :
- ✅ Reçoit des questions en langage naturel
- ✅ Comprend l'intention de la question
- ✅ Répond avec des données mockées réalistes
- ✅ Simule les 5 cas d'usage principaux

**Pas besoin de vraies bases de données pour cette phase !**

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip installé

### Étapes

1. **Cloner/Télécharger le projet**
```bash
cd aerowise_chatbot
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API OpenAI ou Anthropic
```

## 🎮 Utilisation

### Mode CLI (ligne de commande)

```bash
python main.py
```

Exemples de questions à poser :
- "Quels oiseaux ont été observés près de la piste 2 ce mois-ci ?"
- "Donne-moi la description de l'espèce Vanneau huppé"
- "Donne-moi une espèce de plante menacée par l'aéroport"
- "Montre-moi des observations similaires à l'observation #123"
- "Y a-t-il des risques particuliers cette semaine ?"

### Mode Python

```python
from agents.mock_agent import AeroWiseMockAgent

agent = AeroWiseMockAgent()
response = agent.ask("Quels oiseaux près de la piste 2 ?")
print(response)
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/

# Avec couverture
pytest tests/ --cov=agents --cov=models
```

## 📊 Données Mockées

Les données simulées incluent :
- **15 espèces** d'oiseaux et plantes
- **50 observations** géolocalisées
- **8 zones** aéroportuaires (pistes, prairies, zones humides)
- **10 incidents** de bird strikes

## 🔧 Technologies

- **Agno** : Framework d'agents IA
- **Pydantic** : Validation de données
- **Python-dotenv** : Gestion config
- **Pytest** : Tests unitaires

## 📖 Documentation

Voir le document `AeroWise_Chatbot_Specification.docx` pour :
- Architecture détaillée
- Diagrammes
- Plan de développement complet

## 🛣️ Roadmap

- [x] **Phase 1** : MVP avec données mockées ← **VOUS ÊTES ICI**
- [ ] **Phase 2** : Intégration PostGIS
- [ ] **Phase 3** : Multi-agents (Neo4j + Qdrant)
- [ ] **Phase 4** : API + Frontend

## 🤝 Contribution

Projet étudiant BUT Informatique 3ème année.

## 📝 Licence

Projet académique - 2025
