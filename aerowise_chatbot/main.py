"""
AeroWise Chatbot - Point d'entrée principal
Interface CLI pour interagir avec le chatbot
"""
import sys
from agents.mock_agent import AeroWiseMockAgent


def print_banner():
    """Affiche le banner du chatbot"""
    print("\n" + "="*70)
    print("🦉 " + " "*25 + "AEROWISE CHATBOT" + " "*26 + "🦉")
    print("="*70)
    print("Gestion intelligente de la biodiversité aéroportuaire")
    print("Phase 1 - MVP avec données mockées")
    print("="*70 + "\n")


def print_help():
    """Affiche l'aide"""
    print("\n📖 EXEMPLES DE QUESTIONS :")
    print("-" * 70)
    print("  1. Quels oiseaux ont été observés près de la piste 2 ce mois-ci ?")
    print("  2. Donne-moi la description de l'espèce Vanneau huppé")
    print("  3. Donne-moi une espèce de plante menacée par l'aéroport")
    print("  4. Montre-moi des observations similaires à l'observation #5")
    print("  5. Y a-t-il des risques particuliers cette semaine ?")
    print("-" * 70)
    print("\n💡 COMMANDES :")
    print("  - 'help' ou '?' : Afficher cette aide")
    print("  - 'quit' ou 'exit' : Quitter le chatbot")
    print("  - 'stats' : Afficher les statistiques de la base de données")
    print()


def print_stats(agent: AeroWiseMockAgent):
    """Affiche les statistiques de la base de données"""
    print("\n📊 STATISTIQUES DE LA BASE DE DONNÉES")
    print("-" * 70)
    print(f"  Espèces enregistrées     : {len(agent.species)}")
    print(f"    - Oiseaux (Aves)       : {len([s for s in agent.species if s.classe == 'Aves'])}")
    print(f"    - Plantes (Plantae)    : {len([s for s in agent.species if s.classe == 'Plantae'])}")
    print(f"  Observations             : {len(agent.observations)}")
    print(f"  Zones aéroportuaires     : {len(agent.zones)}")
    print(f"  Incidents enregistrés    : {len(agent.incidents)}")
    print(f"    - Gravité élevée       : {len([i for i in agent.incidents if i.gravite == 'élevée'])}")
    print("-" * 70 + "\n")


def main():
    """Fonction principale - Boucle d'interaction"""
    print_banner()
    
    # Initialiser l'agent
    print("⏳ Initialisation de l'agent...")
    try:
        agent = AeroWiseMockAgent()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        sys.exit(1)
    
    print("\n✅ Agent prêt ! Posez vos questions (tapez 'help' pour voir des exemples)\n")
    
    # Boucle d'interaction
    while True:
        try:
            # Lire la question de l'utilisateur
            question = input("🧑 Vous : ").strip()
            
            # Commandes spéciales
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Au revoir ! À bientôt sur AeroWise.\n")
                break
            
            if question.lower() in ['help', '?', 'aide']:
                print_help()
                continue
            
            if question.lower() == 'stats':
                print_stats(agent)
                continue
            
            if not question:
                continue
            
            # Poser la question à l'agent
            print()  # Ligne vide pour la lisibilité
            response = agent.ask(question)
            
            # Afficher la réponse
            print(f"🤖 AeroWise : {response.answer}\n")
            
            # Afficher les métadonnées (en mode debug)
            print(f"📊 [Type: {response.query_type} | Confiance: {response.confidence:.0%} | "
                  f"Temps: {response.execution_time_ms:.0f}ms]\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interruption détectée. Au revoir !\n")
            break
        
        except Exception as e:
            print(f"\n❌ Erreur : {e}\n")
            continue


if __name__ == "__main__":
    main()
