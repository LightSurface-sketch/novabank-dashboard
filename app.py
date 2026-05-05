import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="NovaBank Dashboard", layout="wide")

# =========================
# TITRE + CONTEXTE
# =========================

st.title(" NovaBank — Analyse du churn")

st.markdown("###  Problème")
st.write("Le churn a augmenté de +90% en 6 mois, en lien avec une dégradation de l’expérience digitale.")

st.markdown("---")

# =========================
# DATA
# =========================

mensuel = pd.DataFrame({
    "month": ["Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
    "churn": [2.1, 2.3, 2.8, 3.6, 4.2, 4.0],
    "nps": [41, 39, 34, 25, 19, 21],
    "incidents": [18, 22, 37, 61, 74, 66],
    "complaints": [3200, 3500, 4200, 5600, 6400, 6100]
})

segment = pd.DataFrame({
    "segment": ["Nouveaux", "Jeunes actifs", "Standard", "Premium", "Seniors"],
    "churn": [6.8, 4.5, 3.4, 1.9, 2.6]
})

channel = pd.DataFrame({
    "channel": ["Mobile", "Web", "Call Center", "Agence", "Chatbot"],
    "churn": [5.6, 3.1, 3.9, 1.8, 4.4]
})

# =========================
# KPI
# =========================

st.markdown("###  Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Churn (%)", mensuel["churn"].iloc[-1])
col2.metric("NPS", mensuel["nps"].iloc[-1])
col3.metric("Incidents", mensuel["incidents"].iloc[-1])
col4.metric("Plaintes", mensuel["complaints"].iloc[-1])

st.markdown("---")

# =========================
# GRAPHIQUES TEMPS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Churn dans le temps")
    fig, ax = plt.subplots()
    ax.plot(mensuel["month"], mensuel["churn"])
    ax.set_ylabel("Churn (%)")
    st.pyplot(fig)

with col2:
    st.subheader(" NPS dans le temps")
    fig, ax = plt.subplots()
    ax.plot(mensuel["month"], mensuel["nps"])
    ax.set_ylabel("NPS")
    st.pyplot(fig)

st.markdown(" Le churn augmente fortement tandis que le NPS chute, confirmant une dégradation de l’expérience client.")

st.markdown("---")

# =========================
# ANALYSE SEGMENT / CANAL
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Churn par segment")
    fig, ax = plt.subplots()
    ax.bar(segment["segment"], segment["churn"])
    ax.set_ylabel("Churn (%)")
    plt.xticks(rotation=30)
    st.pyplot(fig)

with col2:
    st.subheader(" Churn par canal")
    fig, ax = plt.subplots()
    ax.bar(channel["channel"], channel["churn"])
    ax.set_ylabel("Churn (%)")
    plt.xticks(rotation=30)
    st.pyplot(fig)

st.markdown(" Les nouveaux clients et le canal mobile sont les plus touchés, ce qui confirme un problème lié à l’expérience digitale.")

st.markdown("---")

# =========================
# RECOMMANDATIONS
# =========================

st.markdown("###  Recommandations")

st.write("""
1. Stabiliser l’application mobile (incidents élevés, churn 5,6%)
2. Réduire les frictions client (plaintes x2, NPS -22 pts)
3. Améliorer l’onboarding des nouveaux clients (churn 6,8%)
""")