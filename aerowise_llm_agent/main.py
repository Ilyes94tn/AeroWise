"""
AeroWise LLM Agent - Interface CLI
Chatbot intelligent avec compréhension du langage naturel
"""
import sys
from agents.llm_agent import AeroWiseLLMAgent


def print_banner():
    """Affiche le banner"""
    print("\n" + "="*70)
    print("🦉 " + " "*20 + "AEROWISE LLM AGENT" + " "*22 + "🦉")
    print("="*70)
    print("Chatbot intelligent - Gestion de la biodiversité aéroportuaire")
    print("Propulsé par OpenAI GPT-4 + Agno")
    print("="*70 + "\n")


def print_help():
    """Affiche l'aide"""
    print("\n📖 EXEMPLES DE QUESTIONS :")
    print("-" * 70)
    print("  ✅ Dans mon domaine :")
    print("     - Parle-moi du Vanneau huppé")
    print("     - Quelles espèces sont menacées?")
    print("     - Quels oiseaux ont un risque de collision élevé?")
    print("     - Donne-moi des infos sur la Corneille noire")
    print()
    print("  ❓ Questions floues (je demanderai des précisions) :")
    print("     - oiseau")
    print("     - espèce")
    print("     - risque")
    print()
    print("  🚫 Hors-sujet (je redirigerai poliment) :")
    print("     - Quelle est la capitale de la France?")
    print("     - Comment faire un gâteau?")
    print("-" * 70)
    print("\n💡 COMMANDES :")
    print("  - 'help' ou '?' : Afficher cette aide")
    print("  - 'quit' ou 'exit' : Quitter")
    print()


def main():
    """Fonction principale"""
    print_banner()
    
    # Initialiser l'agent
    print("⏳ Initialisation de l'agent LLM...")
    print("   (Chargement du modèle OpenAI...)\n")
    
    try:
        agent = AeroWiseLLMAgent()
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\n📝 Pour configurer votre clé API:")
        print("   1. Copiez .env.example vers .env")
        print("   2. Éditez .env et ajoutez votre clé OpenAI")
        print("   3. Relancez le programme\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}\n")
        sys.exit(1)
    
    print("\n✅ Agent prêt ! Posez vos questions (tapez 'help' pour des exemples)\n")
    
    # Boucle d'interaction
    conversation_history = []
    
    while True:
        try:
            # Lire la question
            question = input("🧑 Vous : ").strip()
            
            # Commandes spéciales
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Au revoir ! À bientôt sur AeroWise.\n")
                break
            
            if question.lower() in ['help', '?', 'aide']:
                print_help()
                continue
            
            if not question:
                continue
            
            # Poser la question à l'agent
            print()  # Ligne vide
            print("🤖 AeroWise : ", end="", flush=True)
            
            answer = agent.ask(question)
            print(answer + "\n")
            
            # Sauvegarder dans l'historique
            conversation_history.append({"question": question, "answer": answer})
            
        except KeyboardInterrupt:
            print("\n\n👋 Interruption détectée. Au revoir !\n")
            break
        
        except Exception as e:
            print(f"\n❌ Erreur : {e}\n")
            continue


if __name__ == "__main__":
    main()
