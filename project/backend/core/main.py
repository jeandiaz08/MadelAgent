from src.agents.sql_agent import run_agent

if __name__ == "__main__":
    
    question = "¿Cuánto stock hay en Plaza Sur?"
    
    response = run_agent(question)

    print("\nRespuesta final:")
    print(response)