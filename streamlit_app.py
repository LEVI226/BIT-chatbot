import streamlit as st
from transformers import pipeline
import torch

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Chatbot BIT - Burkina Institute of Technology",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🎓 Chatbot BIT - Assistant virtuel")
st.markdown("**Burkina Institute of Technology - Votre guide académique intelligent**")

# Sidebar avec informations sur BIT
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

# Cache pour le modèle de fallback
@st.cache_resource
def load_fallback_model():
    """Charge le modèle Hugging Face pour le fallback conversationnel"""
    try:
        model = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-small",
            tokenizer="microsoft/DialoGPT-small",
            device=-1,  # CPU only
            pad_token_id=50256
        )
        return model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle: {e}")
        return None

# Base de connaissances BIT (actualisée 2025)
bit_knowledge = {
    "programmes": {
        "génie électrique": "Le programme de Génie Électrique de BIT se concentre sur les énergies renouvelables. Formation de 6 semestres avec stages pratiques.",
        "génie mécanique": "Génie Mécanique avec options Mines et Agriculture. Programme de 6 semestres axé sur l'entrepreneuriat.",
        "informatique": "Science Informatique avec spécialisation en Programmation. Formation pratique en développement et IA.",
        "master intelligence artificielle": "Le Master en Sciences & Technologies, spécialité Intelligence Artificielle, dure 2 ans (4 semestres), enseigné en anglais. Modules : analytics, big data, machine learning, cybersécurité, Tech Lab, entrepreneuriat. Admission : licence en informatique ou équivalent, anglais requis."
    },
    "admission": {
        "prérequis": "Licence (pour le master) ou BAC série C, D, E, S, F2, F3, F4 ou équivalent (pour le bachelor). Test d'anglais et esprit entrepreneurial recommandés.",
        "frais": "Master : 999 000 F CFA/an (+75 000 F CFA de soutenance en 2e année). Paiement échelonné possible.",
        "bourses": "Bourses disponibles selon critères sociaux et mérite académique."
    },
    "campus": {
        "localisation": "Koudougou, région du Centre-Ouest, Burkina Faso.",
        "infrastructure": "Campus moderne conçu par l’architecte Diébédo Francis Kéré, lauréat du Prix Pritzker.",
        "équipements": "Laboratoires modernes, connexion internet haut débit, ordinateurs portables pour étudiants, cité universitaire (10 000 F CFA/mois)."
    },
    "histoire": {
        "fondation": "Fondé en 2017, ouverture officielle en octobre 2018.",
        "fondatrice": "Susanne Pertl.",
        "directeur": "Professeur François Zougmoré.",
        "reconnaissance": "Classé meilleur établissement d'enseignement supérieur privé au Burkina Faso (note 18,10/20, 228 diplômés en 2024)."
    }
}

# Fonction pour chercher dans la base de connaissances
def search_bit_knowledge(query):
    query_lower = query.lower()
    responses = []
    for category, items in bit_knowledge.items():
        if isinstance(items, dict):
            for key, value in items.items():
                if any(word in query_lower for word in key.split()) or any(word in query_lower for word in value.lower().split()):
                    responses.append(f"**{category.title()} - {key.title()}:** {value}")
        else:
            if category in query_lower:
                responses.append(f"**{category.title()}:** {items}")
    return responses

# Fonction pour générer une réponse avec fallback
def generate_fallback_response(query, model):
    """Génère une réponse avec le modèle Hugging Face si aucune info BIT n'est trouvée"""
    if model is None:
        return "Désolé, je ne peux pas répondre à cette question. Posez-moi une question spécifique sur BIT !"
    try:
        context = f"En tant qu'assistant du Burkina Institute of Technology, répondez à cette question: {query}"
        response = model(
            context,
            max_length=100,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=50256
        )
        generated_text = response[0]['generated_text']
        if context in generated_text:
            generated_text = generated_text.replace(context, "").strip()
        return generated_text if generated_text else "Désolé, je ne peux pas répondre à cette question."
    except Exception as e:
        return f"Erreur lors de la génération: {str(e)}"

# Interface de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis l'assistant virtuel de BIT. Comment puis-je vous aider concernant le Burkina Institute of Technology ?"}
    ]

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie utilisateur
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
                    response = f"🤖 **Réponse générée par IA:** {response}\n\n" + """
                    💡 **Information:** Cette réponse a été générée par intelligence artificielle car elle ne concerne pas directement BIT.

                    Pour des informations précises sur BIT, posez-moi des questions sur :
                    - 📚 Programmes d'études (Génie Électrique, Mécanique, Informatique, Master IA)
                    - 📝 Procédures d'admission et prérequis
                    - 🏫 Campus et infrastructure
                    - 💰 Frais de scolarité et bourses
                    - 📞 Contacts et informations pratiques
                    """
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

# Bouton pour effacer l'historique
if st.button("🗑️ Effacer l'historique"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Je suis l'assistant virtuel de BIT. Comment puis-je vous aider concernant le Burkina Institute of Technology ?"}
    ]
    st.rerun()

# Footer
st.markdown("---")
st.markdown("**Développé pour BIT par yannick**")
