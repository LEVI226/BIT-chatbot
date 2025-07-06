# README.md — Chatbot BIT (Burkina Institute of Technology)

## Présentation du projet

Ce projet consiste à développer un **chatbot intelligent** pour le Burkina Institute of Technology (BIT), capable de répondre aux questions sur l’établissement, ses programmes, l’admission, le campus, etc. L’application est réalisée en Python avec **Streamlit** pour l’interface web et un modèle conversationnel **Hugging Face** pour le fallback IA.

- **Technologies principales** : Python, Streamlit, Hugging Face Transformers, DialoGPT-small
- **Déploiement** : Streamlit Cloud

## Fonctionnalités

- **Réponses précises** sur BIT grâce à une base de connaissances structurée (programmes, admission, histoire, localisation…)
- **Fallback IA** : Si la question n’est pas couverte, le chatbot utilise un modèle Hugging Face pour générer une réponse générique
- **Interface utilisateur moderne** : Chat interactif, historique, effacement, sidebar d’information
- **Déploiement cloud** : Application accessible en ligne

## Installation et lancement

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/bit-chatbot.git
   cd bit-chatbot
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l’application localement**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Déploiement**
   - Pousser le code sur GitHub
   - Connecter le repo à Streamlit Cloud
   - Lancer le déploiement via l’interface web

## Structure du projet

```
bit-chatbot/
├── streamlit_app.py
├── requirements.txt
├── README.md
```

## Utilisation

- Posez une question sur BIT dans la zone de chat.
- Le bot répond à partir de la base de connaissances ou, si besoin, via l’IA Hugging Face.
- Utilisez le bouton « Effacer l’historique » pour réinitialiser la conversation.

## Contact

- **BIT** : admissions@bit.bf
- **Site web** : https://bit.bf


