import streamlit as st
from transformers import pipeline
import re

# ... (bit_knowledge et fonctions ci-dessus)

st.set_page_config(
    page_title="Chatbot BIT - Burkina Institute of Technology",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 Chatbot BIT - Assistant virtuel")
st.markdown("**Burkina Institute of Technology - Votre guide académique intelligent**")

with st.sidebar:
    st.header("ℹ️ À propos de BIT")
    st.markdown("""
    **Burkina Institute of Technology** est la première université privée technique du Burkina Faso.

    **📍 Localisation :** Koudougou, Burkina Faso  
    **👤 Directeur général :** Professeur François Zougmoré  
    **🌐 Site web :** https://bit.bf  
    **📞 Contact :** admissions@bit.bf

    **🎓 Programmes :**
    - Génie Électrique (Énergies Renouvelables)
    - Génie Mécanique (Mines et Agriculture)
    - Informatique (Programmation)
    - Master en Intelligence Artificielle (2 ans, anglais)
    """)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis l'assistant virtuel de BIT. Comment puis-je vous aider concernant le Burkina Institute of Technology ?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question sur BIT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Recherche d'informations..."):
            bit_responses = search_bit_knowledge(prompt)
            if bit_responses:
                response = "Voici les informations que j'ai trouvées sur BIT :\n\n" + "\n\n".join(bit_responses)
            else:
                st.info("Aucune information spécifique sur BIT trouvée. Utilisation du modèle IA pour répondre...")
                fallback_model = load_fallback_model()
                if fallback_model:
                    response = generate_fallback_response(prompt, fallback_model)
                    response = f"🤖 **Réponse générée par IA:** {response}\n\n" + '''
                    💡 **Information:** Cette réponse a été générée par intelligence artificielle car elle ne concerne pas directement BIT.

                    Pour des informations précises sur BIT, posez-moi des questions sur :
                    - 📚 Programmes d'études (Génie Électrique, Mécanique, Informatique, Master IA)
                    - 📝 Procédures d'admission et prérequis
                    - 🏫 Campus et infrastructure
                    - 💰 Frais de scolarité et bourses
                    - 📞 Contacts et informations pratiques
                    '''
                else:
                    response = """Je suis spécialisé dans les informations sur le Burkina Institute of Technology (BIT).

Voici ce que je peux vous renseigner :
- 📚 Programmes d'études (Génie Électrique, Mécanique, Informatique, Master IA)
- 📝 Procédures d'admission et prérequis
- 🏫 Campus et infrastructure
- 💰 Frais de scolarité et bourses
- 📞 Contacts et informations pratiques

Posez-moi une question spécifique sur BIT !"""
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("🗑️ Effacer l'historique"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis l'assistant virtuel de BIT. Comment puis-je vous aider concernant le Burkina Institute of Technology ?"}
    ]
    st.rerun()

st.markdown("---")
st.markdown("**Développé pour BIT par yannick**")
