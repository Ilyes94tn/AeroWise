"""
Modèles de données Pydantic pour AeroWise Chatbot
"""
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Coordonnées GPS (latitude, longitude)"""
    lat: float = Field(..., description="Latitude en degrés décimaux")
    lon: float = Field(..., description="Longitude en degrés décimaux")


class Species(BaseModel):
    """Modèle pour une espèce (oiseau ou plante)"""
    id: str = Field(..., description="Identifiant unique")
    nom_scientifique: str = Field(..., description="Nom scientifique (latin)")
    nom_commun: str = Field(..., description="Nom commun en français")
    classe: Literal["Aves", "Plantae"] = Field(..., description="Classe taxonomique")
    description: str = Field(..., description="Description de l'espèce")
    risque_collision: Optional[Literal["faible", "moyen", "élevé"]] = Field(
        None, description="Risque de collision avec aéronefs (pour oiseaux)"
    )
    statut_conservation: Optional[Literal["LC", "NT", "VU", "EN", "CR"]] = Field(
        None, description="Statut IUCN (LC=Préoccupation mineure, CR=En danger critique)"
    )
    habitat_prefere: Optional[str] = Field(None, description="Type d'habitat préféré")


class Zone(BaseModel):
    """Modèle pour une zone aéroportuaire"""
    id: str = Field(..., description="Identifiant unique")
    nom: str = Field(..., description="Nom de la zone")
    type: Literal["piste", "prairie", "zone_humide", "bati", "boisement"] = Field(
        ..., description="Type de zone"
    )
    coordinates: List[Coordinates] = Field(
        ..., description="Polygone définissant la zone (liste de points)"
    )


class Observation(BaseModel):
    """Modèle pour une observation de biodiversité"""
    id: str = Field(..., description="Identifiant unique")
    espece_id: str = Field(..., description="ID de l'espèce observée")
    date: datetime = Field(..., description="Date et heure de l'observation")
    position: Coordinates = Field(..., description="Localisation GPS")
    zone_id: Optional[str] = Field(None, description="ID de la zone où a eu lieu l'observation")
    nombre_individus: int = Field(1, description="Nombre d'individus observés")
    observateur: str = Field(..., description="Nom de l'observateur")
    notes: Optional[str] = Field(None, description="Notes additionnelles")
    photo_url: Optional[str] = Field(None, description="URL de la photo (si disponible)")


class Incident(BaseModel):
    """Modèle pour un incident (bird strike, etc.)"""
    id: str = Field(..., description="Identifiant unique")
    type: Literal["bird_strike", "intrusion_faune", "autre"] = Field(
        ..., description="Type d'incident"
    )
    date: datetime = Field(..., description="Date et heure de l'incident")
    position: Coordinates = Field(..., description="Localisation GPS")
    gravite: Literal["faible", "moyenne", "élevée"] = Field(..., description="Gravité de l'incident")
    espece_impliquee: Optional[str] = Field(None, description="ID de l'espèce impliquée")
    description: str = Field(..., description="Description de l'incident")
    mesures_prises: Optional[str] = Field(None, description="Mesures prises suite à l'incident")


class ChatMessage(BaseModel):
    """Message du chatbot"""
    role: Literal["user", "assistant", "system"] = Field(..., description="Rôle de l'émetteur")
    content: str = Field(..., description="Contenu du message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Horodatage")


class ChatResponse(BaseModel):
    """Réponse du chatbot"""
    answer: str = Field(..., description="Réponse en langage naturel")
    data: Optional[dict] = Field(None, description="Données structurées associées")
    query_type: Literal[
        "spatial", "descriptive", "analytical", "similarity", "alert"
    ] = Field(..., description="Type de requête détectée")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Niveau de confiance")
    execution_time_ms: Optional[float] = Field(None, description="Temps d'exécution en ms")
