# ⚡ Guide de Démarrage Rapide - AeroWise LLM Agent

## 🎯 En 5 minutes chrono !

### 1️⃣ Télécharger et extraire le projet

Extrayez le ZIP dans un dossier de votre choix.

### 2️⃣ Obtenir une clé API OpenAI

1. Allez sur https://platform.openai.com/api-keys
2. Connectez-vous (créez un compte si nécessaire)
3. Cliquez sur "Create new secret key"
4. **Copiez la clé** (vous ne pourrez la voir qu'une fois !)

💡 **Coût** : Environ 0.01€ pour 100 questions avec gpt-4o-mini

### 3️⃣ Installation

Ouvrez un terminal dans le dossier du projet :

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# OU (Windows CMD)
venv\Scripts\activate.bat

# Installer les dépendances
pip install -r requirements.txt
```

### 4️⃣ Configuration de la clé API

**Option A : Avec un éditeur de texte**
1. Renommez `.env.example` en `.env`
2. Ouvrez `.env` avec Notepad
3. Remplacez `sk-votre-cle-api-ici` par votre vraie clé
4. Sauvegardez

**Option B : En ligne de commande** (PowerShell)
```powershell
Copy-Item .env.example .env
# Éditez le fichier .env avec votre clé
```

Votre fichier `.env` doit ressembler à :
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
```

### 5️⃣ Lancer le chatbot !

```bash
python main.py
```

Vous devriez voir :

```
====================================================================
🦉                    AEROWISE LLM AGENT                        🦉
====================================================================
Chatbot intelligent - Gestion de la biodiversité aéroportuaire
Propulsé par OpenAI GPT-4 + Agno
====================================================================

⏳ Initialisation de l'agent LLM...
   (Chargement du modèle OpenAI...)

✅ Agent LLM initialisé
   - Modèle: gpt-4o-mini
   - Données: 6 espèces

✅ Agent prêt ! Posez vos questions (tapez 'help' pour des exemples)

🧑 Vous :
```

---

## 🎮 Testez ces questions

### ✅ Questions intelligentes

```
Parle-moi du Vanneau huppé
Quelles espèces sont menacées?
Quels oiseaux ont un risque de collision élevé?
Donne-moi des infos sur la Corneille noire
```

### ❓ Questions floues (il demandera des précisions)

```
oiseau
espèce
risque
```

### 🚫 Questions hors-sujet (il redirigera poliment)

```
Quelle est la capitale de la France?
Comment faire un gâteau?
Qui a gagné la Coupe du Monde?
```

---

## ❌ Problèmes fréquents

### Erreur "OPENAI_API_KEY manquante"

➡️ Vérifiez que `.env` existe et contient votre clé (pas `.env.example`)

### Erreur "python not found"

➡️ Installez Python 3.10+ : https://www.python.org/downloads/

### Erreur "pip not found"

➡️ Utilisez `python -m pip` au lieu de `pip`

### Erreur "Rate limit exceeded"

➡️ Vous avez dépassé la limite gratuite OpenAI. Ajoutez du crédit sur votre compte.

### Réponses très lentes

➡️ Normal avec GPT-4. Utilisez `gpt-4o-mini` dans `.env` (déjà par défaut)

---

## 🎓 Comprendre le code

### Fichier principal : `agents/llm_agent.py`

**Lignes importantes :**

- **Ligne 28-32** : Configuration OpenAI (clé API, modèle)
- **Ligne 56-150** : Le "system prompt" (instructions pour le LLM)
- **Ligne 235-255** : La fonction `ask()` qui envoie la question à OpenAI

### Personnaliser les réponses

Éditez le `system_prompt` (ligne 56) pour changer :
- Le ton (plus formel / plus décontracté)
- Les exemples de réponses
- Les règles de redirection

---

## 🚀 Prochaines étapes

### Une fois que ça marche

1. **Testez toutes les questions** (voir exemples ci-dessus)
2. **Modifiez le system prompt** pour personnaliser
3. **Ajoutez vos vraies données** (remplacez les JSON dans `/data`)

### Pour aller plus loin

- Ajoutez plus d'espèces dans les fichiers JSON
- Testez avec différents modèles OpenAI
- Ajustez la température pour des réponses plus/moins créatives

---

## 💰 Coûts estimés

Avec **gpt-4o-mini** (recommandé) :

- 100 questions : ~0.01€
- 1000 questions : ~0.10€

Avec **gpt-4o** (plus puissant mais plus cher) :

- 100 questions : ~0.15€
- 1000 questions : ~1.50€

💡 Le crédit gratuit OpenAI (~5$) permet de tester largement !

---

## 🎯 Commandes utiles

```bash
# Lancer le chatbot
python main.py

# Tester l'agent directement
python agents/llm_agent.py

# Vérifier les dépendances
pip list

# Désactiver l'environnement virtuel
deactivate
```

---

## ✅ Checklist avant la démo

- [ ] `.env` créé avec la vraie clé API
- [ ] Le chatbot démarre sans erreur
- [ ] Testé au moins 5 questions différentes
- [ ] Vérifié que les questions hors-sujet sont bien gérées
- [ ] Vérifié que les questions floues demandent des clarifications

---

**Besoin d'aide ?** Lisez le `README.md` complet pour plus de détails !

**Projet SAE - BUT Informatique 3ème année - 2025**
