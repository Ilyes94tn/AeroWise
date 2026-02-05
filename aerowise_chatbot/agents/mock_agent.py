"""
Agent Mock AeroWise - Phase 1 MVP
Répond aux questions avec des données simulées
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from models.schemas import Species, Observation, Zone, Incident, ChatResponse


class AeroWiseMockAgent:
    """
    Agent chatbot avec données mockées pour Phase 1
    Simule les 5 types de requêtes sans vraies bases de données
    """
    
    def __init__(self):
        """Initialise l'agent et charge les données mockées"""
        self.data_dir = Path(__file__).parent.parent / "data"
        
        # Charger les données
        self.species: List[Species] = self._load_json("mock_species.json", Species)
        self.observations: List[Observation] = self._load_json("mock_observations.json", Observation)
        self.zones: List[Zone] = self._load_json("mock_zones.json", Zone)
        self.incidents: List[Incident] = self._load_json("mock_incidents.json", Incident)
        
        print(f"✅ Agent initialisé avec:")
        print(f"   - {len(self.species)} espèces")
        print(f"   - {len(self.observations)} observations")
        print(f"   - {len(self.zones)} zones")
        print(f"   - {len(self.incidents)} incidents")
    
    def _load_json(self, filename: str, model_class):
        """Charge un fichier JSON et le valide avec Pydantic"""
        filepath = self.data_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [model_class(**item) for item in data]
    
    def ask(self, question: str) -> ChatResponse:
        """
        Point d'entrée principal : pose une question à l'agent
        
        Args:
            question: Question en langage naturel
            
        Returns:
            ChatResponse avec la réponse et les données associées
        """
        start_time = datetime.now()
        
        # Analyser le type de question
        query_type = self._detect_query_type(question)
        
        # Router vers la fonction appropriée
        if query_type == "spatial":
            answer, data = self._handle_spatial_query(question)
        elif query_type == "descriptive":
            answer, data = self._handle_descriptive_query(question)
        elif query_type == "analytical":
            answer, data = self._handle_analytical_query(question)
        elif query_type == "similarity":
            answer, data = self._handle_similarity_query(question)
        elif query_type == "alert":
            answer, data = self._handle_alert_query(question)
        else:
            answer = "Je n'ai pas bien compris votre question. Pourriez-vous la reformuler ?"
            data = None
            query_type = "unknown"
        
        # Calculer le temps d'exécution
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return ChatResponse(
            answer=answer,
            data=data,
            query_type=query_type,
            confidence=0.85,
            execution_time_ms=execution_time
        )
    
    def _detect_query_type(self, question: str) -> str:
        """Détecte le type de question posée"""
        q = question.lower()
        
        # Requêtes spatiales (localisation, proximité)
        if any(word in q for word in ["près", "piste", "zone", "secteur", "observés", "où"]):
            return "spatial"
        
        # Requêtes descriptives (description d'espèce)
        if any(word in q for word in ["description", "décris", "qu'est-ce que", "c'est quoi"]):
            return "descriptive"
        
        # Requêtes analytiques (espèces menacées, tendances)
        if any(word in q for word in ["menacé", "danger", "protégé", "conservation", "risque"]):
            return "analytical"
        
        # Recherche de similarité
        if any(word in q for word in ["similaire", "ressemble", "comparable", "proche"]):
            return "similarity"
        
        # Alertes et recommandations
        if any(word in q for word in ["alerte", "risque", "danger", "recommandation", "semaine"]):
            return "alert"
        
        return "unknown"
    
    def _handle_spatial_query(self, question: str) -> tuple[str, Dict]:
        """Gère les requêtes spatiales (ex: oiseaux près de la piste 2)"""
        q = question.lower()
        
        # Déterminer la zone concernée
        target_zone = None
        if "piste 2" in q or "piste deux" in q:
            target_zone = "zone_002"
        elif "piste 1" in q or "piste un" in q:
            target_zone = "zone_001"
        elif "prairie" in q and "nord" in q:
            target_zone = "zone_003"
        elif "zone humide" in q and "est" in q:
            target_zone = "zone_004"
        
        # Filtrer les observations
        if target_zone:
            zone = next((z for z in self.zones if z.id == target_zone), None)
            obs_in_zone = [obs for obs in self.observations if obs.zone_id == target_zone]
            
            # Récupérer les espèces d'oiseaux uniquement
            bird_species_ids = {obs.espece_id for obs in obs_in_zone}
            birds = [sp for sp in self.species if sp.id in bird_species_ids and sp.classe == "Aves"]
            
            if birds:
                bird_names = [f"**{b.nom_commun}** ({b.nom_scientifique})" for b in birds]
                answer = f"Dans la zone **{zone.nom}**, les oiseaux suivants ont été observés récemment :\n\n"
                answer += "\n".join(f"- {name}" for name in bird_names)
                answer += f"\n\n*Total : {len(birds)} espèce(s) observée(s)*"
                
                data = {
                    "zone": zone.dict(),
                    "species": [b.dict() for b in birds],
                    "observation_count": len(obs_in_zone)
                }
            else:
                answer = f"Aucune observation d'oiseau récente dans la zone **{zone.nom}**."
                data = {"zone": zone.dict(), "species": []}
        else:
            # Réponse générique si zone non identifiée
            answer = "Je n'ai pas pu identifier précisément la zone. Voici les 5 observations les plus récentes :\n\n"
            recent_obs = sorted(self.observations, key=lambda x: x.date, reverse=True)[:5]
            
            for obs in recent_obs:
                species = next((s for s in self.species if s.id == obs.espece_id), None)
                zone = next((z for z in self.zones if z.id == obs.zone_id), None)
                answer += f"- **{species.nom_commun}** ({obs.nombre_individus} individu(s)) - {zone.nom} - {obs.date.strftime('%d/%m/%Y')}\n"
            
            data = {
                "observations": [obs.dict() for obs in recent_obs]
            }
        
        return answer, data
    
    def _handle_descriptive_query(self, question: str) -> tuple[str, Dict]:
        """Gère les requêtes descriptives (ex: description d'une espèce)"""
        q = question.lower()
        
        # Chercher une espèce mentionnée dans la question
        target_species = None
        for species in self.species:
            if species.nom_commun.lower() in q or species.nom_scientifique.lower() in q:
                target_species = species
                break
        
        if target_species:
            answer = f"**{target_species.nom_commun}** (*{target_species.nom_scientifique}*)\n\n"
            answer += f"📋 **Description** : {target_species.description}\n\n"
            
            if target_species.classe == "Aves":
                answer += f"⚠️ **Risque de collision** : {target_species.risque_collision or 'Non évalué'}\n"
            
            answer += f"🌍 **Statut de conservation** : {target_species.statut_conservation}\n"
            answer += f"🏞️ **Habitat préféré** : {target_species.habitat_prefere or 'Variable'}"
            
            data = {"species": target_species.dict()}
        else:
            # Si aucune espèce trouvée, proposer une liste
            answer = "Je n'ai pas identifié d'espèce précise dans votre question. Voici quelques espèces disponibles :\n\n"
            sample_species = self.species[:5]
            for sp in sample_species:
                answer += f"- **{sp.nom_commun}** (*{sp.nom_scientifique}*)\n"
            
            data = {"available_species": [sp.dict() for sp in sample_species]}
        
        return answer, data
    
    def _handle_analytical_query(self, question: str) -> tuple[str, Dict]:
        """Gère les requêtes analytiques (ex: espèces menacées)"""
        q = question.lower()
        
        # Chercher des plantes menacées
        if "plante" in q and ("menac" in q or "danger" in q):
            threatened_plants = [
                sp for sp in self.species 
                if sp.classe == "Plantae" and sp.statut_conservation in ["VU", "EN", "CR", "NT"]
            ]
            
            if threatened_plants:
                # Prendre la première
                plant = threatened_plants[0]
                answer = f"Une espèce de plante menacée par l'aéroport est :\n\n"
                answer += f"**{plant.nom_commun}** (*{plant.nom_scientifique}*)\n\n"
                answer += f"📋 {plant.description}\n\n"
                answer += f"⚠️ **Statut de conservation** : {plant.statut_conservation}\n"
                answer += f"🏞️ **Habitat** : {plant.habitat_prefere}\n\n"
                answer += f"*Cette espèce est particulièrement sensible aux activités aéroportuaires " \
                          f"(fauche intensive, drainage, etc.).*"
                
                data = {
                    "species": plant.dict(),
                    "all_threatened_plants": [p.dict() for p in threatened_plants]
                }
            else:
                answer = "Aucune plante menacée identifiée dans la base de données actuelle."
                data = {}
        
        # Chercher des oiseaux à risque élevé
        elif "oiseau" in q or "risque" in q:
            high_risk_birds = [
                sp for sp in self.species 
                if sp.classe == "Aves" and sp.risque_collision == "élevé"
            ]
            
            answer = f"Voici les espèces d'oiseaux à **risque élevé** de collision :\n\n"
            for bird in high_risk_birds:
                answer += f"- **{bird.nom_commun}** (*{bird.nom_scientifique}*) - {bird.description[:80]}...\n"
            
            answer += f"\n*Total : {len(high_risk_birds)} espèce(s) à surveiller prioritairement.*"
            
            data = {"high_risk_species": [b.dict() for b in high_risk_birds]}
        
        else:
            answer = "Je peux vous aider à analyser les espèces menacées ou à risque. " \
                     "Précisez votre recherche (plantes menacées, oiseaux à risque, etc.)"
            data = {}
        
        return answer, data
    
    def _handle_similarity_query(self, question: str) -> tuple[str, Dict]:
        """Gère les requêtes de similarité (ex: observations similaires)"""
        # Pour le MVP, on retourne simplement les observations de la même espèce
        
        # Extraire un ID d'observation si présent
        import re
        obs_id_match = re.search(r'#?(\d+)', question)
        
        if obs_id_match:
            obs_num = obs_id_match.group(1)
            target_obs_id = f"obs_{obs_num.zfill(3)}"
            target_obs = next((obs for obs in self.observations if obs.id == target_obs_id), None)
            
            if target_obs:
                # Trouver d'autres observations de la même espèce
                similar_obs = [
                    obs for obs in self.observations 
                    if obs.espece_id == target_obs.espece_id and obs.id != target_obs.id
                ][:5]
                
                species = next((s for s in self.species if s.id == target_obs.espece_id), None)
                
                answer = f"Observations similaires à l'observation **{target_obs.id}** " \
                         f"(**{species.nom_commun}**) :\n\n"
                
                for obs in similar_obs:
                    zone = next((z for z in self.zones if z.id == obs.zone_id), None)
                    answer += f"- **{obs.id}** - {zone.nom} - {obs.date.strftime('%d/%m/%Y')} " \
                              f"({obs.nombre_individus} individu(s))\n"
                
                if not similar_obs:
                    answer = f"Aucune autre observation de **{species.nom_commun}** trouvée dans la base."
                
                data = {
                    "reference_observation": target_obs.dict(),
                    "similar_observations": [obs.dict() for obs in similar_obs]
                }
            else:
                answer = f"Observation {target_obs_id} non trouvée. Veuillez vérifier l'identifiant."
                data = {}
        else:
            answer = "Pour rechercher des observations similaires, précisez un numéro d'observation (ex: #123)."
            data = {}
        
        return answer, data
    
    def _handle_alert_query(self, question: str) -> tuple[str, Dict]:
        """Gère les requêtes d'alertes (ex: risques cette semaine)"""
        # Compter les incidents récents
        from datetime import timedelta
        
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        recent_incidents = [
            inc for inc in self.incidents 
            if inc.date >= week_ago
        ]
        
        high_severity = [inc for inc in recent_incidents if inc.gravite == "élevée"]
        
        answer = f"📊 **Analyse des risques cette semaine** :\n\n"
        answer += f"- {len(recent_incidents)} incident(s) signalé(s) ces 7 derniers jours\n"
        answer += f"- dont {len(high_severity)} de **gravité élevée**\n\n"
        
        if high_severity:
            answer += "⚠️ **ALERTES** :\n\n"
            for inc in high_severity:
                species = next((s for s in self.species if s.id == inc.espece_impliquee), None)
                species_name = species.nom_commun if species else "Espèce non identifiée"
                answer += f"- **{inc.date.strftime('%d/%m/%Y')}** : {inc.description} ({species_name})\n"
            
            answer += "\n**Recommandation** : Renforcer la surveillance et l'effarouchement dans les zones à risque."
        else:
            answer += "✅ Pas d'alerte critique cette semaine. Maintenir la vigilance habituelle."
        
        data = {
            "recent_incidents": [inc.dict() for inc in recent_incidents],
            "high_severity_count": len(high_severity),
            "total_count": len(recent_incidents)
        }
        
        return answer, data


if __name__ == "__main__":
    # Test rapide de l'agent
    agent = AeroWiseMockAgent()
    
    test_questions = [
        "Quels oiseaux ont été observés près de la piste 2 ce mois-ci ?",
        "Donne-moi la description du Vanneau huppé",
        "Donne-moi une espèce de plante menacée par l'aéroport",
        "Montre-moi des observations similaires à l'observation #5",
        "Y a-t-il des risques particuliers cette semaine ?"
    ]
    
    print("\n" + "="*60)
    print("🧪 TEST DE L'AGENT MOCK")
    print("="*60 + "\n")
    
    for question in test_questions:
        print(f"❓ {question}\n")
        response = agent.ask(question)
        print(f"💬 {response.answer}\n")
        print(f"📊 Type: {response.query_type} | Confiance: {response.confidence} | " 
              f"Temps: {response.execution_time_ms:.0f}ms\n")
        print("-" * 60 + "\n")
