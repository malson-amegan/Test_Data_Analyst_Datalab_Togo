# 🇹🇬 Optimisation du Réseau de Services Publics au Togo
**Candidat :** Malson AMEGAN | **Rôle :** Data Analyst (Test Pratique)

## 📌 Contexte du Projet
Ce projet vise à analyser la délivrance des documents officiels (CNI, Passeports, Actes de naissance) au Togo. L'objectif est d'identifier les zones de saturation, d'évaluer l'équité territoriale et de proposer des recommandations basées sur la donnée.

## 🛠️ Stack Technique
- **Analyse :** Python (Pandas, Matplotlib, Seaborn)
- **Calculs :** SQL (Requêtes de pilotage KPI)
- **Visualisation :** Streamlit (Dashboard interactif)
- **Versionnage :** Git / GitHub

## 📂 Structure du Dépôt
- `notebooks/` : Analyse exploratoire (EDA) et nettoyage des données.
- `scripts/` : Code source du Dashboard interactif.
- `KPIs/` : Définition, objectifs et règles de calcul des 6 indicateurs clés.
- `reports/` : Rapport de synthèse et présentation PowerPoint destinée aux décideurs.

## 🚀 Installation et Utilisation
1. Cloner le dépôt : `git clone https://github.com/ton-profil/test-datalab.git`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer le dashboard : `streamlit run scripts/app_dashboard.py`

## 💡 Principaux Enseignements
- **Délai moyen :** 23 jours (Le passeport est le document le plus critique).
- **Alerte :** Le centre CT054 présente un temps d'attente moyen de 119 minutes.
- **Accessibilité :** Corrélation forte entre infrastructure électrique et taux de rejet des dossiers.