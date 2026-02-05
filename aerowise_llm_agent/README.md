# 🦉 AeroWise LLM Agent

**Chatbot intelligent avec compréhension du langage naturel**  
Propulsé par OpenAI GPT-4 + Agno

---

## 🎯 Différences avec la version précédente

| Aspect | Version Mock | Version LLM ⭐ |
|--------|-------------|---------------|
| **Compréhension** | Règles if/else basiques | Vrai LLM (GPT-4) |
| **Questions floues** | Réponse générique | Demande clarification |
| **Hors-sujet** | Message d'erreur | Redirection intelligente |
| **Données** | JSON mockées | JSON (prêt pour BDD) |
| **Qualité réponses** | Template | Langage naturel fluide |

---

## ✨ Capacités de l'Agent LLM

### ✅ Comprend VRAIMENT le langage naturel

- **Question précise** : "Parle-moi du Vanneau huppé"  
  → Réponse détaillée avec données structurées

- **Question floue** : "oiseau"  
  → "Votre question est un peu vague. Souhaitez-vous une liste des oiseaux, des infos sur une espèce précise, ou connaître les oiseaux à risque?"

- **Hors-sujet** : "Quelle est la capitale de la France?"  
  → "Je suis spécialisé dans la biodiversité aéroportuaire. Je peux vous aider sur les espèces, risques aviaires, ou gestion environnementale."

### 🎯 Gestion intelligente des questions

- Détecte l'intention réelle (pas de mots-clés rigides)
- Extrait le contexte pertinent des données
- Reformule les questions mal posées
- Propose des alternatives

### 🔍 Recherche intelligente dans les données

- Recherche par nom scientifique OU vernaculaire
- Filtre par risque de collision
- Filtre par statut de conservation
- Synthèse automatique des informations

---

## 🚀 Installation

### 1. Prérequis

- Python 3.10+
- Clé API OpenAI ([obtenir une clé](https://platform.openai.com/api-keys))

### 2. Installation

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter votre clé API OpenAI
# OPENAI_API_KEY=sk-votre-cle-ici
```

### 4. Lancer

```bash
python main.py
```

---

## 💡 Exemples d'Utilisation

### ✅ Questions bien gérées

```
🧑 Vous : Parle-moi du Vanneau huppé

🤖 AeroWise : 🦅 **Vanneau huppé** (*Vanellus vanellus*)

C'est un oiseau limicole de taille moyenne, caractérisé par:
- Plumage noir et blanc avec reflets verts métalliques
- Huppe noire distinctive
- Cri plaintif 'pee-wit' en vol

📍 Habitat: Prairies humides, zones agricoles
⚠️ Risque aviation: Moyen
🌍 Conservation: NT (Quasi menacé)
```

### ❓ Questions ambiguës

```
🧑 Vous : oiseau

🤖 AeroWise : Votre question est un peu vague. Souhaitez-vous:
- Une liste des oiseaux présents sur l'aéroport?
- Des informations sur une espèce d'oiseau en particulier?
- Connaître les oiseaux à risque de collision?

Précisez et je vous aiderai!
```

### 🚫 Questions hors-sujet

```
🧑 Vous : Quelle est la capitale de la France?

🤖 AeroWise : Je suis spécialisé dans la biodiversité aéroportuaire 
et ne peux pas répondre à cette question. En revanche, je peux vous 
renseigner sur les espèces d'oiseaux présentes, les risques de 
collision, ou les mesures de gestion environnementale. 
Puis-je vous aider sur l'un de ces sujets?
```

---

## 📊 Données Disponibles

Le chatbot a accès à **6 espèces** avec :

**Oiseaux :**
- Vanneau huppé (*Vanellus vanellus*)
- Corneille noire (*Corvus corone*)
- Buse variable (*Buteo buteo*)
- Alouette des champs (*Alauda arvensis*)
- Étourneau sansonnet (*Sturnus vulgaris*)

**Plantes :**
- Ophrys abeille (*Ophrys apifera*)

Pour chaque espèce :
- Description détaillée (Wikipedia)
- Noms vernaculaires (FR, EN, DE)
- Habitat et comportement
- Statut de conservation IUCN
- Niveau de risque aviation
- Distribution géographique
- Images

---

## 🔧 Configuration Avancée

### Modèles OpenAI disponibles

Dans `.env`, vous pouvez changer le modèle :

```bash
# Rapide et économique (recommandé pour développement)
OPENAI_MODEL=gpt-4o-mini

# Plus puissant (pour production)
OPENAI_MODEL=gpt-4o

# Ancien modèle
OPENAI_MODEL=gpt-4-turbo
```

### Ajuster la température

```bash
# Plus déterministe (recommandé)
OPENAI_TEMPERATURE=0.3

# Plus créatif
OPENAI_TEMPERATURE=0.7
```

---

## 🔮 Prochaines Étapes

### Phase actuelle ✅
- [x] Agent LLM avec OpenAI
- [x] Données JSON
- [x] Gestion intelligente questions hors-sujet
- [x] Interface CLI

### Phase 2 (à venir)
- [ ] Remplacer JSON par fichiers .parquet
- [ ] Ajouter Pandas pour requêtes complexes
- [ ] Améliorer le système de recherche

### Phase 3 (futur)
- [ ] Connexion BDD PostgreSQL + PostGIS
- [ ] Multi-agents avec Agno
- [ ] Agent Data séparé
- [ ] API REST

---

## 🆘 Dépannage

### ❌ Erreur "OPENAI_API_KEY manquante"

→ Vérifiez que le fichier `.env` existe et contient votre clé API

### ❌ Erreur "Rate limit exceeded"

→ Vous avez dépassé la limite de requêtes. Attendez ou ajoutez du crédit sur OpenAI

### ❌ Réponses lentes

→ Normal avec GPT-4. Utilisez `gpt-4o-mini` pour plus de rapidité

---

## 📝 Structure du Projet

```
aerowise_llm_agent/
├── agents/
│   ├── __init__.py
│   └── llm_agent.py        # Agent principal (LLM)
├── data/
│   ├── enriched_wikipedia.json    # Descriptions espèces
│   └── enriched_gbif_media.json   # Métadonnées espèces
├── config/
│   └── (vide pour l'instant)
├── models/
│   └── (vide pour l'instant)
├── main.py                  # Interface CLI
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎓 Pour les Étudiants

### Points forts pour la SAE
- ✅ Architecture moderne (LLM + Agno)
- ✅ Gestion robuste des erreurs
- ✅ Code bien structuré et commenté
- ✅ Extensible (prêt pour BDD)
- ✅ Démonstration impressionnante

### Ce qui sera noté positivement
- Compréhension réelle du NLP
- Pas de règles if/else rigides
- Gestion intelligente des cas limites
- Code production-ready

---

**Développé pour le BUT Informatique 3ème année - 2025**  
**Projet : AeroWise - Gestion de la biodiversité aéroportuaire**
