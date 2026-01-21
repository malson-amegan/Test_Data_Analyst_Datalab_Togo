import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.set_page_config(layout="wide", page_title="Datalab Togo - Pilotage des Services Publics")


# Style CSS pour améliorer l'esthétique
st.markdown("""
<style>
    /* Conteneur principal des cartes */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 20px;
    }
    /* Style individuel de chaque carte */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        flex: 1;
        border-top: 5px solid #000; /* Sera surchargé par la couleur du KPI */
    }
    .kpi-label {
        font-size: 14px;
        color: #6c757d;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #1f1f1f;
    }
</style>
""", unsafe_allow_html=True)

def kpi_card(label, value, color):
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 5px solid {color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

#  CHARGEMENT ET NETTOYAGE DES DONNÉES
@st.cache_data
def load_data():
    # REMPLACE CES CHEMINS par tes chemins locaux sur VS Code 
    path = "./" 
    
    dfs = {
        'logs': pd.read_csv(path + 'logs_activite.csv'),
        'centres': pd.read_csv(path + 'centres_service.csv'),
        'demandes': pd.read_csv(path + 'demandes_service_public.csv'),
        'communes': pd.read_csv(path + 'details_communes.csv'),
        'dev': pd.read_csv(path + 'developpement.csv'),
        'socio': pd.read_csv(path + 'donnees_socioeconomiques.csv')
    }

    # Nettoyage rapide
    dfs['logs']['date_operation'] = pd.to_datetime(dfs['logs']['date_operation'])
    dfs['demandes']['date_demande'] = pd.to_datetime(dfs['demandes']['date_demande'])
    
    return dfs

try:
    data = load_data()
except FileNotFoundError:
    st.error("Erreur : Fichiers CSV non trouvés. Vérifiez les chemins dans la fonction load_data().")
    st.stop()

# BARRE LATÉRALE 
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Flag_of_Togo.svg/1200px-Flag_of_Togo.svg.png", width=100)
st.sidebar.title("Filtres Décisionnels")
regions = ["Toutes"] + list(data['centres']['region'].unique())
selected_region = st.sidebar.selectbox("Filtrer par Région", regions)

#  Application du filtre 
if selected_region != "Toutes":
    df_demandes = data['demandes'][data['demandes']['region'] == selected_region]
    df_centres = data['centres'][data['centres']['region'] == selected_region]
    df_dev = data['dev'][data['dev']['region'] == selected_region]
    
    # On identifie la colonne ID (probablement centre_id au lieu de id_centre)
    col_id = 'centre_id' if 'centre_id' in df_centres.columns else 'id_centre'
    
    list_centres = df_centres[col_id].unique()
    # On filtre les logs pour ne garder que les centres de la région sélectionnée
    df_logs = data['logs'][data['logs']['centre_id'].isin(list_centres)]
else:
    df_demandes, df_centres, df_dev, df_logs = data['demandes'], data['centres'], data['dev'], data['logs']

# TITRE ET MÉTRIQUES GLOBALES
st.title("Pilotage National des Services Publics")
st.markdown(f"**Analyse actuelle :** {selected_region}")

# Section des métriques améliorées
m1, m2, m3, m4 = st.columns(4)

with m1:
    kpi_card("Délai Moyen", f"{df_demandes['delai_traitement_jours'].mean():.1f} Jours", "#007bff") # Bleu

with m2:
    kpi_card("Centres Actifs", f"{len(df_centres)} Sites", "#28a745") # Vert

with m3:
    kpi_card("Taux de Rejet", f"{df_demandes['taux_rejet'].mean()*100:.1f} %", "#dc3545") # Rouge

with m4:
    kpi_card("Productivité", f"{(df_logs['nombre_traite'].sum()/df_logs['personnel_present'].sum()):.1f} Doc/Agt", "#6f42c1") # Violet

st.markdown("---")

# GRAPHIQUES 
col_a, col_b = st.columns(2)

with col_a:
    # KPI 1 : DMT
    st.subheader("1. Délais par Type de Document")
    dmt = df_demandes.groupby('type_document', observed=False)['delai_traitement_jours'].mean().sort_values()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=dmt.values, y=dmt.index, palette="Blues_d", ax=ax1)
    st.pyplot(fig1)

    # KPI 3 : Nombre de centres
    st.subheader("3. Couverture : Centres par Région")
    nb_centres = df_centres.groupby('region').size().sort_values(ascending=False)
    fig3, ax3 = plt.subplots()
    sns.barplot(x=nb_centres.index, y=nb_centres.values, palette="Greens_d", ax=ax3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # KPI 5 : Taux de Rejet
    st.subheader("5. Qualité : Taux de Rejet par Région")
    rejet = df_demandes.groupby('region')['taux_rejet'].mean().sort_values(ascending=False)
    fig5, ax5 = plt.subplots()
    sns.barplot(x=rejet.index, y=rejet.values, palette="Reds_d", ax=ax5)
    plt.xticks(rotation=45)
    st.pyplot(fig5)

with col_b:
    # KPI 2 : Temps d'Attente
    st.subheader("2. Attente Moyenne par Centre (Top 10)")
    attente = df_logs.groupby('centre_id')['temps_attente_moyen_minutes'].mean().sort_values(ascending=False).head(10)
    fig2, ax2 = plt.subplots()
    sns.barplot(x=attente.values, y=attente.index, palette="Oranges_d", ax=ax2)
    st.pyplot(fig2)

    # KPI 4 : Accès Électricité
    st.subheader("4. Infrastructure : Accès Électricité")
    elec = df_dev.groupby('region')['acces_electricite'].mean().sort_values(ascending=False)
    fig4, ax4 = plt.subplots()
    sns.barplot(x=elec.index, y=elec.values, palette="Purples_d", ax=ax4)
    plt.xticks(rotation=45)
    st.pyplot(fig4)

    # KPI 6 : Productivité
    st.subheader("6. Productivité par Centre (Top 10)")
    prod = (df_logs.groupby('centre_id')['nombre_traite'].sum() / df_logs.groupby('centre_id')['personnel_present'].sum()).sort_values(ascending=False).head(10)
    fig6, ax6 = plt.subplots()
    sns.barplot(x=prod.values, y=prod.index, palette="YlGnBu", ax=ax6)
    st.pyplot(fig6)

    #  SECTION 2 : LES DEUX ANALYSES DE L'IMAGE 3 
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📍 Répartition des Centres par Région")
    # Données basées sur ton image
    df_pie = pd.DataFrame({
        'Région': ['Centrale', 'Maritime', 'Kara', 'Savanes', 'Plateaux'],
        'Valeur': [29.1, 27.3, 18.2, 14.5, 10.9]
    })
    fig_pie = px.pie(df_pie, values='Valeur', names='Région', hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    fig_pie.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.markdown("### 💡 Accessibilité vs Qualité")
    # Données de corrélation basées sur ton graphique à bulles
    df_scatter = pd.DataFrame({
        'Région': ['Maritime', 'Centrale', 'Kara', 'Plateaux', 'Savanes'],
        'Électricité (%)': [85.6, 80.0, 75.0, 73.0, 71.0],
        'Taux Rejet (%)': [7.2, 7.6, 7.0, 7.3, 7.6]
    })
    fig_scatter = px.scatter(df_scatter, x='Électricité (%)', y='Taux Rejet (%)', 
                             text='Région', size='Électricité (%)', color='Région',
                             color_discrete_sequence=px.colors.qualitative.Set1)
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
<div style="background-color: #e6f4ea; padding: 20px; border-radius: 10px; border-left: 5px solid #1e8e3e;">
    <strong>💡 Insight Stratégique :</strong> On remarque une corrélation entre l'infrastructure (électricité) et la qualité. 
    La région des Savanes nécessite un renforcement urgent de l'accessibilité.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.success("💡 Recommandation stratégique : Focaliser la digitalisation sur les zones à forte attente (KPI 2) et faible productivité (KPI 6).")