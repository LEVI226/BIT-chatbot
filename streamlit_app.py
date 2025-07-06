import streamlit as st
from transformers import pipeline
import re

# Base de connaissances BIT (actualisée 2025)
bit_knowledge = {
    "localisation": "BIT est situé à Koudougou, Burkina Faso. Adresse : 322 Koudougou, Burkina Faso.",
    "signification": "BIT signifie Burkina Institute of Technology.",
    "histoire": "Fondé en 2017, BIT a ouvert officiellement en octobre 2018. Fondatrice : Susanne Pertl. Directeur général actuel : Professeur François Zougmoré.",
    "reconnaissance": "BIT a été classé meilleur établissement d'enseignement supérieur privé du Burkina Faso (note 18,10/20, 228 diplômés en 2024).",
    "programmes": {
        "génie électrique": "Licence en Génie Électrique et Énergies Renouvelables (6 semestres, stages pratiques, enseignement en anglais).",
        "génie mécanique": "Licence en Génie Mécanique, options Mécanisation Agricole ou Mines (6 semestres, pédagogie entrepreneuriale, anglais).",
        "informatique": "Licence en Informatique et Entrepreneuriat (6 semestres, développement logiciel, IA, anglais).",
        "master intelligence artificielle": "Master en Sciences & Technologies, spécialité Intelligence Artificielle (2 ans, anglais, modules ML, big data, cybersécurité, Tech Lab, entrepreneuriat). Admission : licence en informatique ou équivalent, anglais requis."
    },
    "admission": {
        "licence": "BAC C, D, E, S, F1, F2, F3, F4 ou équivalent. Test d'anglais et entretien oral. Dossier : lettre de motivation, CNIB, acte de naissance, diplôme BAC, relevés de notes, photos, justificatif de revenus.",
        "master": "Licence en informatique ou équivalent, compétences en anglais, esprit entrepreneurial. Test d'anglais et entretien oral.",
        "frais_licence": "1ère année : 550 000 F CFA, 2ème année : 550 000 F CFA, 3ème année : 600 000 F CFA + 75 000 F CFA soutenance. Paiement en 3 fois possible.",
        "frais_master": "999 000 F CFA/an + 75 000 F CFA soutenance (2e année). Paiement échelonné possible.",
        "bourses": "Bourses disponibles selon critères sociaux et mérite académique."
    },
    "campus": {
        "infrastructure": "Campus moderne conçu par Diébédo Francis Kéré, lauréat du Prix Pritzker. Laboratoires, connexion internet haut débit, ordinateurs portables pour étudiants.",
        "hébergement": "Cité universitaire ouverte d’octobre à juillet, loyer 10 000 F CFA/mois, cantine disponible.",
        "partenariats": "BIT collabore avec des entreprises nationales et internationales pour les stages et l'insertion professionnelle."
    },
    "contact": "admissions@bit.bf, https://bit.bf, Tel : 00226 53 11 11 10"
}

# Fonction de recherche intelligente dans la base de connaissances
def search_bit_knowledge(query):
    query_lower = query.lower()
    responses = []
    # Recherche directe dans les clés principales
    for key, value in bit_knowledge.items():
        if isinstance(value, dict):
            for subkey, subval in value.items():
                if subkey in query_lower or any(word in query_lower for word in re.split(r'\\W+', subkey)):
                    responses.append(f"**{subkey.title()} :** {subval}")
        else:
            if key in query_lower or any(word in query_lower for word in re.split(r'\\W+', key)):
                responses.append(f"**{key.title()} :** {value}")
    # Recherche contextuelle sur les questions courantes
    if not responses:
        if any(word in query_lower for word in ["où", "localisation", "adresse"]):
            responses.append(f"**Localisation :** {bit_knowledge['localisation']}")
        if any(word in query_lower for word in ["signifie", "acronyme", "que veut dire"]):
            responses.append(f"**Signification :** {bit_knowledge['signification']}")
        if any(word in query_lower for word in ["directeur", "président", "responsable"]):
            responses.append(f"**Directeur :** Professeur François Zougmoré")
    return responses

# Chargement du modèle Hugging Face pour le fallback IA
@st.cache_resource
def load_fallback_model():
    try:
        model = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-small",
            tokenizer="microsoft/DialoGPT-small",
            device=-1,
            pad_token_id=50256
        )
        return model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle: {e}")
        return None

def generate_fallback_response(query, model):
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

# Configuration de la page Streamlit
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
