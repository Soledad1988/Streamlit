import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

st.title("📈 Volumen de Tickets")

# Fondo de toda la página
page_bg = """
<style>
    .stApp {
        background-color: #E0E0E0; /* gris oscuro */
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

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

# ⚠️ MUY IMPORTANTE:
# Necesitás cargar el dataset igual que en la página principal
df = pd.read_excel("Data\IT_Support_Ticket_Spanish.xlsx")

# Volvemos a aplicar los mismos filtros (Streamlit recuerda las selecciones en sidebar)
# ----------------- Filtros en la barra lateral -----------------
with st.sidebar:
    st.header("🔍 Filtros")

    # País
    parPais = st.multiselect(
        "🌍 País",
        options=df['País'].unique(),
    )

    # Categoría
    parCategoria = st.multiselect(
        "📂 Categoría",
        options=df['Categoría'].unique(),
    )

    # Tipo
    parTipo = st.multiselect(
        "🎫 Tipo de Ticket",
        options=df['Tipo'].unique(),
    )

    # Prioridad
    parPrioridad = st.multiselect(
        "⚠️ Prioridad",
        options=df['Prioridad'].unique(),
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

# ----------------- CONTENIDO DE ESTA PÁGINA -----------------

# Calculos
# Calcular tabla por País
# -----------------------------------------

# Aseguramos que las fechas estén en formato datetime
df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
df_filtrado['Fecha de Resolución'] = pd.to_datetime(df_filtrado['Fecha de Resolución'])

# Crear columna duración en días
df_filtrado['Duración (días)'] = (
    df_filtrado['Fecha de Resolución'] - df_filtrado['Fecha']
).dt.total_seconds() / (3600*24)

# Agrupar por País
tabla_paises = (
    df_filtrado
    .groupby("País")
    .agg(
        Total_Problemas = ("ID de Ticket", "count"),
        Tiempo_Promedio_Resolucion = ("Duración (días)", "mean")
    )
    .reset_index()
)

# Redondear el promedio a 2 decimales
tabla_paises["Tiempo_Promedio_Resolucion"] = tabla_paises["Tiempo_Promedio_Resolucion"].round(2)

#-------------------------------------------------------------------------------

# Declaramos 2 columnas en una proporción de 50% y 50%
c1, c2 = st.columns([50,50])

with c1:
    # Volumen de Tickets por pais
    # Agrupar y contar tickets por País
    volumen_trabajo = df_filtrado['País'].value_counts().sort_values(ascending=True)

    # Normalizar valores entre 0 y 1 para aplicar el colormap
    norm = mcolors.Normalize(vmin=min(volumen_trabajo.values), vmax=max(volumen_trabajo.values))

    # Elegir colormap (ej: "Blues", "Greens", "Oranges", "Purples", etc.)
    cmap = cm.get_cmap("Blues")

    # Generar colores según los valores
    bar_colors = [cmap(norm(value)) for value in volumen_trabajo.values]

    # Graficar horizontal con colores
    fig1, ax = plt.subplots(figsize=(6,4), facecolor="none")
    bars = plt.barh(volumen_trabajo.index, volumen_trabajo.values, color=bar_colors)

    # Etiquetas y título
    plt.title("Volumen de Tickets por País")

    # Poner etiquetas al final de cada barra usando width
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width - (width*0.05),   # un poco adentro de la barra                          # posición x (al final de la barra)
            bar.get_y() + bar.get_height()/2,   # posición y (centro de la barra)
            str(width),                         # el valor
            va='center', ha='right', color='black', fontweight='bold'            # alineación
        )

    ax.set_facecolor("#E0E0E0")  # el área del gráfico en gris
    plt.tight_layout()
    st.pyplot(fig1)

with c2:
    # Mostrar en columnas
    # -----------------------------------------
    # Mostrar tabla en Streamlit
    st.dataframe(tabla_paises.sort_values("Total_Problemas", ascending=False))
    
    height=300,   # alto fijo
    use_container_width=True  # ajusta al ancho de la columna


# Declaramos 2 columnas en una proporción de 50% y 50%
c1, c2 = st.columns([50,50])

with c1:
    # Contar cantidad de tickets por Etiqueta Primaria y tomar solo los 9 primeros
    tickets_por_etiqueta = df_filtrado['Etiqueta Primaria'].value_counts().head(9)

    # Gráfico de barras
    fig2, ax = plt.subplots(figsize=(6,4), facecolor="none")
    bars = plt.bar(tickets_por_etiqueta.index, tickets_por_etiqueta.values)

    # Etiquetas y título
    plt.title("Top 9 Etiquetas Primarias con más Tickets")

    # Mostrar valores dentro de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,   # posición X centrada
            height/2,                          # posición Y a la mitad de la barra
            str(height),                       # valor
            ha='center', va='center',          # alineación centrada
            color='black', fontweight='bold'   # estilo para contraste
        )

    plt.xticks(rotation=45)  # rotar etiquetas si son largas
    plt.tight_layout()
    ax.set_facecolor("#E0E0E0")  # el área del gráfico en gris
    st.pyplot(fig2)

with c2:
    # Prioridad por Cantidad Tickets
    # Agrupar tickets por Prioridad
    prioridad_counts = df_filtrado['Prioridad'].value_counts()

    # Normalizar valores para mapear a un colormap
    norm = mcolors.Normalize(vmin=min(prioridad_counts.values), vmax=max(prioridad_counts.values))

    cmap = cm.get_cmap("tab20")  

    # Generar lista de colores según los valores
    colors = [cmap(norm(value)) for value in prioridad_counts.values]

    # Gráfico de pastel
    fig3 = plt.figure(figsize=(5,3), facecolor="none")
    plt.pie(prioridad_counts,
            labels=prioridad_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
            colors=colors)
    ax.set_facecolor("#E0E0E0")  # el área del gráfico en gris
    plt.title("Distribución de Tickets por Prioridad")
    plt.axis('equal')  # mantiene proporciones
    st.pyplot(fig3)