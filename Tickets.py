import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

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
# ----------------- Contenedor para gráficos -----------------
chart_card_style = """
    <div style="padding:20px;
                border-radius:15px;
                text-align:center;
                margin-top:30px;      /* <-- Espacio antes de empezar */
                margin-bottom:20px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        {}
    </div>
"""

# Declaramos 2 columnas en una proporción de 50% y 50%
c1, c2 = st.columns([50,50])

with c1:
    # Frecuencia de tipos de tickets , color="#1f77b4"
    frecuencia_tickets = df_filtrado['Tipo'].value_counts().sort_values(ascending=False)

    fig1, ax1= plt.subplots(figsize=(8,5),facecolor="none")

    # Normalizar valores entre 0 y 1 para aplicar el colormap
    norm = mcolors.Normalize(vmin=min(frecuencia_tickets.values), vmax=max(frecuencia_tickets.values))

    # Elegir colormap (ej: Blues, Oranges, Greens, Purples, etc.)
    cmap = cm.get_cmap("Blues")

    # Generar colores según los valores
    bar_colors = [cmap(norm(value)) for value in frecuencia_tickets.values]
    bars = ax1.bar(frecuencia_tickets.index, frecuencia_tickets.values, color = bar_colors)

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
    ax1.set_facecolor("#E0E0E0")  # el área del gráfico en gris
    st.pyplot(fig1)

with c2:
    # Agrupar y contar tickets por Cola
    carga_trabajo = df_filtrado['Cola'].value_counts().sort_values(ascending=True)

    fig2, ax2 = plt.subplots(figsize=(7,6), facecolor="none")

    bars = ax2.barh(carga_trabajo.index, carga_trabajo.values)

    ax2.set_title("Cola de soporte con mayor carga de trabajo")

    # Etiquetas en las barras
    for bar in bars:
        width = bar.get_width()
        ax2.text(width - (width*0.05),   # un poco adentro de la barra
                bar.get_y() + bar.get_height()/2,
                str(width),
                va='center', ha='right', color='black', fontweight='bold')

    ax2.set_facecolor("#E0E0E0")  # el área del gráfico en gris
    st.pyplot(fig2)

# Declaramos 2 columnas en una proporción de 50% y 50%
c1, c2 = st.columns([50,50])

with c1:
    # Calcular la diferencia en días para cada ticket
    df_filtrado['Duración (días)'] = (df_filtrado['Fecha de Resolución'] - df_filtrado['Fecha']).dt.total_seconds() / (3600*24)

    # Agrupar por prioridad y calcular el promedio
    promedio_por_prioridad = df_filtrado.groupby('Prioridad')['Duración (días)'].mean().sort_values(ascending=False)

    # Graficar barras verticales
    fig3, ax = plt.subplots(figsize=(8,5), facecolor="none")

    bars = plt.bar(promedio_por_prioridad.index, promedio_por_prioridad.values)

    plt.title("Tiempo promedio de resolución por prioridad")

    # Etiquetas arriba de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f"{height:.2f}", ha='center', va='bottom')
    
    ax.set_facecolor("#E0E0E0")  # el área del gráfico en gris
    st.pyplot(fig3)

with c2:
    # Tiempo promedio de resolución por tipo
    # Calcular la diferencia en días para cada ticket
    df_filtrado['Duración (días)'] = (df_filtrado['Fecha de Resolución'] - df_filtrado['Fecha']).dt.total_seconds() / (3600*24)

    # Agrupar por prioridad y calcular el promedio
    promedio_por_tipo = df_filtrado.groupby('Tipo')['Duración (días)'].mean().sort_values(ascending=False)

    # Graficar barras verticales
    fig4, ax = plt.subplots(figsize=(8,5), facecolor="none")


    # Normalizar valores entre 0 y 1 para aplicar el colormap
    norm = mcolors.Normalize(vmin=min(frecuencia_tickets.values), vmax=max(frecuencia_tickets.values))

    # Elegir colormap (ej: Blues, Oranges, Greens, Purples, etc.)
    cmap = cm.get_cmap("Blues")

    # Generar colores según los valores
    bar_colors = [cmap(norm(value)) for value in frecuencia_tickets.values]

    bars = plt.bar(promedio_por_tipo.index, promedio_por_tipo.values, color = bar_colors)

    plt.title("Tiempo promedio de resolución por prioridad")

    # Etiquetas arriba de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f"{height:.2f}", ha='center', va='bottom')
    
    ax.set_facecolor("#E0E0E0")  # el área del gráfico en gris  
    st.pyplot(fig4)