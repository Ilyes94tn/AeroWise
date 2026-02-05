"""
Tests unitaires pour AeroWiseMockAgent
"""
import pytest
from agents.mock_agent import AeroWiseMockAgent


@pytest.fixture
def agent():
    """Fixture pour créer une instance de l'agent"""
    return AeroWiseMockAgent()


class TestQueryTypeDetection:
    """Tests de détection du type de requête"""
    
    def test_detect_spatial_query(self, agent):
        """Test détection requête spatiale"""
        question = "Quels oiseaux près de la piste 2 ?"
        query_type = agent._detect_query_type(question)
        assert query_type == "spatial"
    
    def test_detect_descriptive_query(self, agent):
        """Test détection requête descriptive"""
        question = "Donne-moi la description du Vanneau huppé"
        query_type = agent._detect_query_type(question)
        assert query_type == "descriptive"
    
    def test_detect_analytical_query(self, agent):
        """Test détection requête analytique"""
        question = "Quelles plantes sont menacées ?"
        query_type = agent._detect_query_type(question)
        assert query_type == "analytical"
    
    def test_detect_similarity_query(self, agent):
        """Test détection requête similarité"""
        question = "Observations similaires à #123"
        query_type = agent._detect_query_type(question)
        assert query_type == "similarity"
    
    def test_detect_alert_query(self, agent):
        """Test détection requête alerte"""
        question = "Y a-t-il des risques cette semaine ?"
        query_type = agent._detect_query_type(question)
        assert query_type == "alert"


class TestSpatialQueries:
    """Tests des requêtes spatiales"""
    
    def test_spatial_query_piste_2(self, agent):
        """Test requête spatiale sur piste 2"""
        response = agent.ask("Quels oiseaux près de la piste 2 ?")
        
        assert response.query_type == "spatial"
        assert response.confidence > 0.8
        assert "piste" in response.answer.lower() or "zone" in response.answer.lower()
        assert response.data is not None
    
    def test_spatial_query_generic(self, agent):
        """Test requête spatiale générique"""
        response = agent.ask("Quelles observations récentes ?")
        
        assert response.query_type == "spatial"
        assert response.data is not None


class TestDescriptiveQueries:
    """Tests des requêtes descriptives"""
    
    def test_descriptive_query_vanneau(self, agent):
        """Test description du Vanneau huppé"""
        response = agent.ask("Donne-moi la description du Vanneau huppé")
        
        assert response.query_type == "descriptive"
        assert "Vanneau" in response.answer
        assert "description" in response.answer.lower() or "plumage" in response.answer.lower()
        assert response.data is not None
        assert "species" in response.data
    
    def test_descriptive_query_unknown_species(self, agent):
        """Test description d'une espèce inconnue"""
        response = agent.ask("Décris-moi le Dragon de Komodo")
        
        assert response.query_type == "descriptive"
        # Doit proposer des alternatives
        assert "espèces disponibles" in response.answer.lower()


class TestAnalyticalQueries:
    """Tests des requêtes analytiques"""
    
    def test_analytical_query_threatened_plants(self, agent):
        """Test recherche plantes menacées"""
        response = agent.ask("Donne-moi une espèce de plante menacée par l'aéroport")
        
        assert response.query_type == "analytical"
        assert "plante" in response.answer.lower()
        assert response.data is not None
    
    def test_analytical_query_high_risk_birds(self, agent):
        """Test recherche oiseaux à risque"""
        response = agent.ask("Quels oiseaux ont un risque de collision élevé ?")
        
        assert response.query_type == "analytical"
        assert "risque" in response.answer.lower()


class TestSimilarityQueries:
    """Tests des requêtes de similarité"""
    
    def test_similarity_query_valid_id(self, agent):
        """Test similarité avec ID valide"""
        response = agent.ask("Montre-moi des observations similaires à #5")
        
        assert response.query_type == "similarity"
        assert response.data is not None
    
    def test_similarity_query_without_id(self, agent):
        """Test similarité sans ID"""
        response = agent.ask("Observations similaires")
        
        assert response.query_type == "similarity"
        assert "précisez un numéro" in response.answer.lower()


class TestAlertQueries:
    """Tests des requêtes d'alertes"""
    
    def test_alert_query_weekly(self, agent):
        """Test alertes hebdomadaires"""
        response = agent.ask("Y a-t-il des risques particuliers cette semaine ?")
        
        assert response.query_type == "alert"
        assert "incident" in response.answer.lower() or "alerte" in response.answer.lower()
        assert response.data is not None
        assert "recent_incidents" in response.data


class TestDataLoading:
    """Tests du chargement des données"""
    
    def test_species_loaded(self, agent):
        """Vérifier que les espèces sont chargées"""
        assert len(agent.species) > 0
        assert all(hasattr(sp, 'nom_commun') for sp in agent.species)
    
    def test_observations_loaded(self, agent):
        """Vérifier que les observations sont chargées"""
        assert len(agent.observations) > 0
        assert all(hasattr(obs, 'espece_id') for obs in agent.observations)
    
    def test_zones_loaded(self, agent):
        """Vérifier que les zones sont chargées"""
        assert len(agent.zones) > 0
        assert all(hasattr(zone, 'nom') for zone in agent.zones)
    
    def test_incidents_loaded(self, agent):
        """Vérifier que les incidents sont chargés"""
        assert len(agent.incidents) > 0
        assert all(hasattr(inc, 'gravite') for inc in agent.incidents)


class TestResponseFormat:
    """Tests du format de réponse"""
    
    def test_response_has_required_fields(self, agent):
        """Vérifier que la réponse contient tous les champs requis"""
        response = agent.ask("Test question")
        
        assert hasattr(response, 'answer')
        assert hasattr(response, 'query_type')
        assert hasattr(response, 'confidence')
        assert hasattr(response, 'execution_time_ms')
        
        assert isinstance(response.answer, str)
        assert 0.0 <= response.confidence <= 1.0
    
    def test_execution_time_measured(self, agent):
        """Vérifier que le temps d'exécution est mesuré"""
        response = agent.ask("Test question")
        
        assert response.execution_time_ms is not None
        assert response.execution_time_ms >= 0


# Tests de performance (optionnels)
class TestPerformance:
    """Tests de performance basiques"""
    
    def test_response_time_under_threshold(self, agent):
        """Vérifier que le temps de réponse est acceptable"""
        response = agent.ask("Quels oiseaux près de la piste 2 ?")
        
        # Le temps de réponse devrait être < 100ms pour des données mockées
        assert response.execution_time_ms < 1000, \
            f"Temps de réponse trop long: {response.execution_time_ms}ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
