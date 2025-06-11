import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import asyncio
import time

# Charger les variables d'environnement
load_dotenv(dotenv_path=".env")

# Configurer l'interface Streamlit
st.title("Chat avec l'agent MCP")
st.write("Posez votre question à l'agent intelligent")

# Initialisation de l'agent
@st.cache_resource
def initialize_agent():
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

# Initialiser l'agent une seule fois
agent = initialize_agent()

# Initialiser l'historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis votre assistant IA. Comment puis-je vous aider aujourd'hui ?"}
    ]

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fonction pour exécuter l'agent avec mémoire
async def run_agent_with_memory(messages):
    # Formater les messages pour l'agent
    formatted_messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in messages
    ]
    
    response = await agent.ainvoke({
        "messages": formatted_messages
    })
    
    # Récupérer le contenu du dernier message AI
    return response['messages'][-1].content

# Gestion des entrées utilisateur
if prompt := st.chat_input("Posez votre question ici"):
    # Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message utilisateur
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Préparer l'espace pour la réponse de l'assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simuler un streaming pour une meilleure expérience utilisateur
        with st.spinner("L'agent réfléchit..."):
            # Exécuter l'agent de manière asynchrone
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Passer tout l'historique des messages à l'agent
                response = loop.run_until_complete(run_agent_with_memory(st.session_state.messages))
                
                # Simuler l'effet de streaming
                for chunk in response.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                
                message_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"⚠️ Erreur: {str(e)}"
                message_placeholder.markdown(full_response)
            finally:
                loop.close()
        
    # Ajouter la réponse de l'assistant à l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})