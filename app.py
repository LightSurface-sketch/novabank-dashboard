import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="NovaBank Dashboard", layout="wide")

# =========================
# LOAD DATA
# =========================

file = r"C:\Users\utilisateur\Desktop\novabank\novabank_etude_de_cas_donnees.xlsx"

mensuel = pd.read_excel(file, sheet_name="mensuel")
segment = pd.read_excel(file, sheet_name="segment")
channel = pd.read_excel(file, sheet_name="channel")

# =========================
# CLEAN DATA
# =========================

def clean(col):
    return col.astype(str).str.replace(",", ".").astype(float)

mensuel["churn_rate_pct"] = clean(mensuel["churn_rate_pct"])
mensuel["mobile_login_success_pct"] = clean(mensuel["mobile_login_success_pct"])
mensuel["avg_wait_time_min"] = clean(mensuel["avg_wait_time_min"])

segment["churn_rate_pct"] = clean(segment["churn_rate_pct"])
segment["complaint_rate_pct"] = clean(segment["complaint_rate_pct"])

channel["incident_rate_pct"] = clean(channel["incident_rate_pct"])
channel["churn_rate_pct"] = clean(channel["churn_rate_pct"])

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Filtres")

selected_month = st.sidebar.selectbox("Choisir un mois", mensuel["month"])

# =========================
# DATA FILTER
# =========================

data = mensuel[mensuel["month"] == selected_month].iloc[0]

# =========================
# HEADER
# =========================

st.title(" NovaBank — Pilotage du churn")

st.markdown(f"""
###  Mois sélectionné : **{selected_month}**
Dégradation de l'expérience digitale = hausse du churn
""")

st.markdown("---")

# =========================
# KPI
# =========================

idx = mensuel[mensuel["month"] == selected_month].index[0]

def delta(col):
    if idx == 0:
        return 0
    return mensuel[col].iloc[idx] - mensuel[col].iloc[idx-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Churn (%)", round(data["churn_rate_pct"],2), round(delta("churn_rate_pct"),2))
col2.metric("NPS", int(data["nps"]), int(delta("nps")))
col3.metric("Incidents", int(data["app_incidents_count"]), int(delta("app_incidents_count")))
col4.metric("Plaintes", int(data["complaints_count"]), int(delta("complaints_count")))

st.markdown("---")

# =========================
# GRAPHIQUES (SÉPARÉS)
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Évolution du churn")
    fig, ax = plt.subplots()
    ax.plot(mensuel["month"], mensuel["churn_rate_pct"], marker="o")
    ax.set_ylabel("Churn (%)")
    st.pyplot(fig)

with col2:
    st.subheader(" Évolution du NPS")
    fig, ax = plt.subplots()
    ax.plot(mensuel["month"], mensuel["nps"], marker="o")
    ax.set_ylabel("NPS")
    st.pyplot(fig)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Incidents applicatifs")
    fig, ax = plt.subplots()
    ax.plot(mensuel["month"], mensuel["app_incidents_count"], marker="o")
    ax.set_ylabel("Incidents")
    st.pyplot(fig)

with col2:
    st.subheader(" Plaintes clients")
    fig, ax = plt.subplots()
    ax.plot(mensuel["month"], mensuel["complaints_count"], marker="o")
    ax.set_ylabel("Plaintes")
    st.pyplot(fig)

st.markdown("---")

# =========================
# SEGMENTS / CANAUX
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn par segment")
    fig, ax = plt.subplots()
    ax.bar(segment["segment"], segment["churn_rate_pct"])
    plt.xticks(rotation=30)
    st.pyplot(fig)

with col2:
    st.subheader(" Churn par canal")
    fig, ax = plt.subplots()
    ax.bar(channel["service_channel"], channel["churn_rate_pct"])
    plt.xticks(rotation=30)
    st.pyplot(fig)

st.markdown("---")

# =========================
# RECOMMANDATIONS
# =========================

st.subheader("Actions prioritaires")

st.write("""
1. Stabiliser l’application mobile  
2. Réduire les frictions client (incidents + support)  
3. Améliorer l’onboarding des nouveaux clients  
""")
