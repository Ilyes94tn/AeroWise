"""
Agent LLM Intelligent - AeroWise
Utilise Claude (Anthropic) pour comprendre le langage naturel
et répondre intelligemment aux questions sur la biodiversité aéroportuaire
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from anthropic import Anthropic

# Charger les variables d'environnement
load_dotenv()


class AeroWiseLLMAgent:
    """
    Agent intelligent basé sur Claude (Anthropic) pour la gestion de biodiversité aéroportuaire
    
    Caractéristiques:
    - Comprend le langage naturel (pas de règles if/else)
    - Interroge des données JSON (future: BDD)
    - Gère intelligemment les questions hors-sujet
    - Demande des clarifications si nécessaire
    """
    
    def __init__(self):
        """Initialise l'agent LLM et charge les données"""
        # Configuration Anthropic Claude
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY manquante dans .env")
        
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")
        self.temperature = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("ANTHROPIC_MAX_TOKENS", "1000"))
        
        # Client Anthropic
        self.client = Anthropic(api_key=self.api_key)
        
        # Charger les données
        self.data_dir = Path(__file__).parent.parent / "data"
        self.wikipedia_data = self._load_json("enriched_wikipedia.json")
        self.gbif_data = self._load_json("enriched_gbif_media.json")
        
        print(f"✅ Agent LLM initialisé (Claude Anthropic)")
        print(f"   - Modèle: {self.model}")
        print(f"   - Données: {len(self.wikipedia_data)} espèces")
        
        # Créer le system prompt
        self._create_system_prompt()
    
    def _load_json(self, filename: str) -> List[Dict]:
        """Charge un fichier JSON"""
        filepath = self.data_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_system_prompt(self):
        """Crée le system prompt pour Claude"""
        
        # Créer un résumé des données disponibles
        species_list = [
            f"- {sp['scientific_name']} ({self._get_french_name(sp['species_key'])})"
            for sp in self.wikipedia_data
        ]
        
        self.system_prompt = f"""Tu es AeroWise, un assistant IA spécialisé dans la gestion de la biodiversité aéroportuaire.

CONTEXTE ET DONNÉES DISPONIBLES:
Tu as accès à une base de données contenant {len(self.wikipedia_data)} espèces:
{chr(10).join(species_list)}

Pour chaque espèce, tu disposes de:
- Descriptions détaillées (Wikipedia)
- Noms vernaculaires en plusieurs langues
- Informations sur l'habitat et le comportement
- Statut de conservation
- Niveau de risque pour l'aviation (pour les oiseaux)
- Distribution géographique
- Images

TON RÔLE:
1. Répondre aux questions sur la biodiversité aéroportuaire
2. Fournir des informations précises basées sur tes données
3. Aider à la gestion des risques aviaires
4. Éduquer sur les espèces présentes

DIRECTIVES IMPORTANTES:

🎯 QUESTIONS DANS TON DOMAINE:
- Réponds de manière claire, précise et professionnelle
- Utilise les données disponibles pour étayer tes réponses
- Si tu as l'information, fournis-la directement
- Cite tes sources quand c'est pertinent (ex: "Selon les données GBIF...")

❓ QUESTIONS AMBIGUËS OU INCOMPLÈTES:
- Demande gentiment des précisions
- Propose des options si plusieurs interprétations sont possibles
- Exemple: "Voulez-vous savoir quels oiseaux sont présents près d'une piste spécifique, ou tous les oiseaux observés sur l'aéroport?"

🚫 QUESTIONS HORS-SUJET (sans rapport avec la biodiversité aéroportuaire):
- Réponds poliment que tu es spécialisé dans la biodiversité aéroportuaire
- Propose de rediriger vers ton domaine d'expertise
- Exemple: "Je suis spécialisé dans la biodiversité aéroportuaire. Je peux vous renseigner sur les espèces présentes, les risques aviaires, ou la gestion environnementale. Puis-je vous aider sur un de ces sujets?"

STYLE DE COMMUNICATION:
- Professionnel mais accessible
- Utilise des émojis occasionnellement (🦅, 🌿, ⚠️, ✅) pour la clarté
- Sois concis mais complet
- Structure tes réponses (points, paragraphes courts)

EXEMPLES DE BONNES RÉPONSES:

Q: "Quelle est la capitale de la France?"
R: "Je suis spécialisé dans la biodiversité aéroportuaire et ne peux pas répondre à cette question. En revanche, je peux vous renseigner sur les espèces d'oiseaux présentes dans les aéroports français, les risques de collision, ou les mesures de gestion environnementale. Puis-je vous aider sur l'un de ces sujets?"

Q: "oiseau"
R: "Votre question est un peu vague. Souhaitez-vous:
- Une liste des oiseaux présents sur l'aéroport?
- Des informations sur une espèce d'oiseau en particulier?
- Connaître les oiseaux à risque de collision?
Précisez et je vous aiderai!"

Q: "Parle-moi du Vanneau huppé"
R: "🦅 **Vanneau huppé** (*Vanellus vanellus*)

C'est un oiseau limicole de taille moyenne, caractérisé par:
- Plumage noir et blanc avec reflets verts métalliques
- Huppe noire distinctive
- Cri plaintif 'pee-wit' en vol

📍 Habitat: Prairies humides, zones agricoles
⚠️ Risque aviation: Moyen
🌍 Conservation: NT (Quasi menacé)

Il niche au sol et se nourrit d'invertébrés. Présent en France, Allemagne et Royaume-Uni."

RÈGLE D'OR:
Si une question concerne la biodiversité, l'écologie, les oiseaux, les plantes, les risques aviaires, ou la gestion environnementale aéroportuaire → RÉPONDS
Sinon → REDIRIGE poliment vers ton domaine"""
    
    def _get_french_name(self, species_key: int) -> str:
        """Récupère le nom français d'une espèce"""
        gbif_entry = next((sp for sp in self.gbif_data if sp['species_key'] == species_key), None)
        if gbif_entry:
            french_names = [n['name'] for n in gbif_entry['vernacular_names'] if n['language'] == 'fr']
            if french_names:
                return french_names[0]
        return "Nom français indisponible"
    
    def _build_context_for_llm(self, user_question: str) -> str:
        """
        Construit le contexte pertinent pour Claude
        basé sur la question de l'utilisateur
        """
        context_parts = []
        
        # Analyser la question pour extraire des mots-clés
        question_lower = user_question.lower()
        
        # Chercher des espèces mentionnées
        for wiki_sp in self.wikipedia_data:
            sci_name = wiki_sp['scientific_name'].lower()
            if sci_name in question_lower or any(word in sci_name for word in question_lower.split()):
                gbif_sp = next((sp for sp in self.gbif_data if sp['species_key'] == wiki_sp['species_key']), None)
                
                french_name = self._get_french_name(wiki_sp['species_key'])
                
                context_parts.append(f"""
ESPÈCE: {wiki_sp['scientific_name']} ({french_name})
Description Wikipedia: {wiki_sp['extract_text']}
Statut conservation: {gbif_sp.get('conservation_status') if gbif_sp else 'N/A'}
Risque aviation: {gbif_sp.get('risk_level') if gbif_sp else 'N/A'}
""")
        
        # Si "risque" ou "dangereux" dans la question
        if any(word in question_lower for word in ['risque', 'danger', 'collision', 'élevé']):
            high_risk = [sp for sp in self.gbif_data if sp.get('risk_level') == 'élevé']
            if high_risk and not context_parts:
                context_parts.append("ESPÈCES À RISQUE ÉLEVÉ:")
                for sp in high_risk[:3]:
                    french_name = self._get_french_name(sp['species_key'])
                    context_parts.append(f"- {sp['scientific_name']} ({french_name})")
        
        # Si "menacé" ou "protégé" dans la question
        if any(word in question_lower for word in ['menac', 'protég', 'conservation', 'vulnérable']):
            threatened_statuses = ['VU', 'EN', 'CR', 'NT']
            threatened = [sp for sp in self.gbif_data if sp.get('conservation_status') in threatened_statuses]
            if threatened and not context_parts:
                context_parts.append("ESPÈCES MENACÉES:")
                for sp in threatened[:3]:
                    french_name = self._get_french_name(sp['species_key'])
                    wiki_sp = next((w for w in self.wikipedia_data if w['species_key'] == sp['species_key']), None)
                    desc = wiki_sp['extract_text'][:200] + "..." if wiki_sp else "Description indisponible"
                    context_parts.append(f"- {sp['scientific_name']} ({french_name}): {desc}")
        
        # Si pas de contexte trouvé, donner un aperçu général
        if not context_parts:
            context_parts.append("DONNÉES DISPONIBLES: Informations sur 6 espèces (oiseaux et plantes) avec descriptions complètes.")
        
        return "\n".join(context_parts)
    
    def ask(self, question: str) -> str:
        """
        Pose une question à l'agent Claude
        
        Args:
            question: Question en langage naturel
            
        Returns:
            Réponse de l'agent en langage naturel
        """
        # Construire le contexte pertinent
        context = self._build_context_for_llm(question)
        
        # Construire le message utilisateur avec contexte
        user_message = f"""CONTEXTE DES DONNÉES DISPONIBLES:
{context}

QUESTION DE L'UTILISATEUR:
{question}

Réponds à cette question en utilisant le contexte fourni et en suivant tes directives."""
        
        try:
            # Appeler l'API Claude (Anthropic)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"❌ Erreur lors de la communication avec l'API Claude: {str(e)}\n\nVérifiez que votre clé API Anthropic est correcte dans le fichier .env"


if __name__ == "__main__":
    # Test rapide
    agent = AeroWiseLLMAgent()
    
    test_questions = [
        "Parle-moi du Vanneau huppé",
        "Quelle est la capitale de la France?",
        "oiseau",
        "Quelles espèces sont menacées?",
        "Risques de collision élevés?"
    ]
    
    print("\n" + "="*70)
    print("🧪 TEST DE L'AGENT LLM (Claude)")
    print("="*70 + "\n")
    
    for q in test_questions:
        print(f"❓ {q}\n")
        answer = agent.ask(q)
        print(f"🤖 {answer}\n")
        print("-"*70 + "\n")
