import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Transactions", layout="wide")

st.title("📊 Dashboard des Transactions Mobiles")
st.markdown("Exploration interactive des transactions, fraudes, produits et fournisseurs.")

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv("Transactions_data_complet (1).csv")
    df["TransactionStartTime"] = pd.to_datetime(df["TransactionStartTime"])
    df["Date"] = pd.to_datetime(df["TransactionStartTime"].dt.date)
    df["FraudResultLabel"] = df["FraudResult"].map({0: "Normale", 1: "Frauduleuse"})
    return df

df = load_data()

# Filtres
st.sidebar.header("🎛️ Filtres")
selected_product = st.sidebar.multiselect("Catégorie de produit", df["ProductCategory"].unique(), default=df["ProductCategory"].unique())
selected_provider = st.sidebar.multiselect("Fournisseur", df["ProviderId"].unique(), default=df["ProviderId"].unique())

filtered_df = df[(df["ProductCategory"].isin(selected_product)) & (df["ProviderId"].isin(selected_provider))]

# Graphiques
tab1, tab2, tab3, tab4 = st.tabs(["📦 Catégories", "💰 Fournisseurs", "📆 Temps", "⚠️ Fraudes"])

with tab1:
    st.subheader("Transactions par catégorie de produit")
    fig1 = px.histogram(filtered_df, x="ProductCategory", color="FraudResultLabel", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Montants par fournisseur")
    fig2 = px.box(filtered_df, x="ProviderId", y="Amount", points="all")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Nombre de transactions par jour")
    df_per_day = filtered_df.groupby("Date").size().reset_index(name="Transactions")
    fig3 = px.line(df_per_day, x="Date", y="Transactions")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("Répartition des fraudes")
    fraud_df = filtered_df["FraudResultLabel"].value_counts().reset_index()
    fraud_df.columns = ["FraudResult", "Count"]
    fig4 = px.pie(fraud_df, values="Count", names="FraudResult")
    st.plotly_chart(fig4, use_container_width=True)
