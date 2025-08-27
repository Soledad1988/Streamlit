import pandas as pd
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

#-------------------------------------------------------------------------------
# Pasar fecha a formato datetime
df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
df_filtrado['Fecha de Resolución'] = pd.to_datetime(df_filtrado['Fecha de Resolución'])

# Crear columna de diferencia
df_filtrado['Tiempo de Resolución'] = df_filtrado['Fecha de Resolución'] - df_filtrado['Fecha']

# ----------------- Cálculos -----------------
total_ticket = df_filtrado['ID de Ticket'].count()
tiempo_promedio_resolucion = df_filtrado['Tiempo de Resolución'].mean()
tiempo_promedio_dias = round(tiempo_promedio_resolucion.total_seconds() / (3600*24), 2)
cantidad_alta = df_filtrado[df_filtrado['Prioridad'] == 'high'].shape[0]

# ----------------- Tarjetas -----------------
c1, c2, c3 = st.columns(3)

# Fondo de toda la página
page_bg = """
<style>
    .stApp {
        background-color: #E0E0E0; /* gris oscuro */
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Estilo de tarjeta (HTML + CSS inline)
card_style = """
    <div style="background-color:#1E1E1E;
                padding:20px;
                border-radius:15px;
                text-align:center;
                margin-bottom:25px;   /* <-- Espacio extra */
                box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        <h3 style="color:#FFD700; font-size:22px;">{}</h3>
        <h2 style="color:white; font-size:36px; margin-top:-10px;">{}</h2>
    </div>
"""

with c1:
    st.markdown(card_style.format("🎫 Total de Tickets", total_ticket), unsafe_allow_html=True)

with c2:
    st.markdown(card_style.format("⏱️ Tiempo promedio (días)", tiempo_promedio_dias), unsafe_allow_html=True)

with c3:
    st.markdown(card_style.format("⚠️ Tickets Alta Prioridad", cantidad_alta), unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------
# ----------------- Estilo global de Matplotlib -----------------
plt.style.use("dark_background")  # Fondo oscuro
custom_color = "#FFD700"  # Dorado para títulos y etiquetas

# ----------------- Contenedor para gráficos -----------------
chart_card_style = """
    <div style="background-color:#1E1E1E;
                padding:20px;
                border-radius:15px;
                text-align:center;
                margin-top:20px;      /* <-- Espacio antes de empezar */
                margin-bottom:20px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        {}
    </div>
"""

# Declaramos 2 columnas en una proporción de 50% y 50%
c1, c2 = st.columns([50,50])

with c1:
    # Frecuencia de tipos de tickets
    frecuencia_tickets = df_filtrado['Tipo'].value_counts().sort_values(ascending=False)

    fig1, ax1 = plt.subplots(figsize=(8,5))
    bars = ax1.bar(frecuencia_tickets.index, frecuencia_tickets.values, color="#1f77b4")

    #ax1.set_xlabel("Tipo de Ticket")
    #ax1.set_ylabel("Frecuencia")
    ax1.set_title("Frecuencia de Tipos de Tickets")

    # Etiquetas en las barras
    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width()/2,
            height,
            str(height),
            ha='center', va='bottom'
        )

    st.pyplot(fig1)

with c2:
    # Agrupar y contar tickets por Cola
    carga_trabajo = df_filtrado['Cola'].value_counts().sort_values(ascending=True)

    fig2, ax2 = plt.subplots(figsize=(7,6))
    bars = ax2.barh(carga_trabajo.index, carga_trabajo.values, color="#1f77b4")

    #ax2.set_xlabel("Cantidad de Tickets")
    #ax2.set_ylabel("Cola de Soporte")
    ax2.set_title("Cola de soporte con mayor carga de trabajo")

    # Etiquetas en las barras
    for bar in bars:
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
                 str(width), va='center')

    st.pyplot(fig2)

# Declaramos 2 columnas en una proporción de 50% y 50%
c1, c2 = st.columns([50,50])

with c1:
    # Calcular la diferencia en días para cada ticket
    df_filtrado['Duración (días)'] = (df_filtrado['Fecha de Resolución'] - df_filtrado['Fecha']).dt.total_seconds() / (3600*24)

    # Agrupar por prioridad y calcular el promedio
    promedio_por_prioridad = df_filtrado.groupby('Prioridad')['Duración (días)'].mean().sort_values(ascending=False)

    # Graficar barras verticales
    fig3 = plt.figure(figsize=(8,5))
    bars = plt.bar(promedio_por_prioridad.index, promedio_por_prioridad.values)

    #plt.ylabel("Tiempo promedio de resolución (días)")
    #plt.xlabel("Prioridad")
    plt.title("Tiempo promedio de resolución por prioridad")

    # Etiquetas arriba de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f"{height:.2f}", ha='center', va='bottom')
    st.pyplot(fig3)

with c2:
    # Tiempo promedio de resolución por tipo
    # Calcular la diferencia en días para cada ticket
    df_filtrado['Duración (días)'] = (df_filtrado['Fecha de Resolución'] - df_filtrado['Fecha']).dt.total_seconds() / (3600*24)

    # Agrupar por prioridad y calcular el promedio
    promedio_por_tipo = df_filtrado.groupby('Tipo')['Duración (días)'].mean().sort_values(ascending=False)

    # Graficar barras verticales
    fig4 = plt.figure(figsize=(8,5))
    bars = plt.bar(promedio_por_tipo.index, promedio_por_tipo.values)

    #plt.ylabel("Tiempo promedio de resolución")
    #plt.xlabel("Tipo")
    plt.title("Tiempo promedio de resolución por prioridad")

    # Etiquetas arriba de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f"{height:.2f}", ha='center', va='bottom')
    st.pyplot(fig4)