import pandas as od
import streamlit as st
import matplotlib.pyplot as plt

#------------------------------Dashboard
st.set_page_config(
    page_title="Tickets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Optimización del rendimiento del soporte de TI")

# Cargamos el dataset
df = pd.read_excel("C:/Users/brent/Downloads/IT_Support_Ticket_Spanish.xlsx")

# ----------------- Filtros en la barra lateral -----------------
with st.sidebar:
    st.header("🔍 Filtros")

    # País
    parPais = st.multiselect(
        "🌍 País",
        options=df['País'].unique(),
        #default=df['País'].unique()  # todos seleccionados por defecto
    )

    # Categoría
    parCategoria = st.multiselect(
        "📂 Categoría",
        options=df['Categoría'].unique(),
        #default=df['Categoría'].unique()
    )

    # Tipo
    parTipo = st.multiselect(
        "🎫 Tipo de Ticket",
        options=df['Tipo'].unique(),
        #default=df['Tipo'].unique()
    )

    # Prioridad
    parPrioridad = st.multiselect(
        "⚠️ Prioridad",
        options=df['Prioridad'].unique(),
        #default=df['Prioridad'].unique()
    )

# ----------------- Aplicar filtros al dataframe -----------------
df_filtrado = df.copy()

if parPais:
    df_filtrado = df_filtrado[df_filtrado['País'].isin(parPais)]

if parCategoria:
    df_filtrado = df_filtrado[df_filtrado['Categoría'].isin(parCategoria)]

if parTipo:
    df_filtrado = df_filtrado[df_filtrado['Tipo'].isin(parTipo)]

if parPrioridad:
    df_filtrado = df_filtrado[df_filtrado['Prioridad'].isin(parPrioridad)]

# ----------------- Aplicar filtros al dataframe -----------------
df_filtrado = df.copy()

if parPais:
    df_filtrado = df_filtrado[df_filtrado['País'].isin(parPais)]

if parCategoria:
    df_filtrado = df_filtrado[df_filtrado['Categoría'].isin(parCategoria)]

if parTipo:
    df_filtrado = df_filtrado[df_filtrado['Tipo'].isin(parTipo)]

if parPrioridad:
    df_filtrado = df_filtrado[df_filtrado['Prioridad'].isin(parPrioridad)]