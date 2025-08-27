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