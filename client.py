import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio

# Charger les variables d'environnement
load_dotenv(dotenv_path=".env")

# Configurer l'interface Streamlit
st.title("Chat avec l'agent MCP")
st.write("Posez votre question à l'agent intelligent")

# Initialisation de l'agent (version synchrone)
@st.cache_resource
def initialize_agent():
    # Créer un nouvel event loop pour les opérations async
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def _initialize():
        client = MultiServerMCPClient(
            {
                "local_mcp": {
                    "url": "http://127.0.0.1:8000/mcp",
                    "transport": "streamable_http",
                }
            }
        )
        tools = await client.get_tools()
        return create_react_agent("openai:gpt-4o-mini", tools)
    
    return loop.run_until_complete(_initialize())

# Fonction pour exécuter l'agent
async def run_agent(question, agent):
    response = await agent.ainvoke({
        "messages": [{
            "role": "user", 
            "content": question
        }]
    })
    # Supposons que la réponse est dans le dernier message de type 'assistant'
    return response['messages'][-1].content

# Initialiser l'agent une seule fois
agent = initialize_agent()

# Interface utilisateur
user_input = st.text_input("Votre question:", key="user_input")

if st.button("Envoyer") and user_input:
    with st.spinner("L'agent réfléchit..."):
        # Exécuter l'agent de manière asynchrone
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(run_agent(user_input, agent))
            
            # Afficher la réponse
            st.write("Réponse de l'agent:")
            st.write(response)
        finally:
            loop.close()