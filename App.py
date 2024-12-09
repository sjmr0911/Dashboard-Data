import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar datos
data = pd.read_csv("Extended_Employee_Performance_and_Productivity_Data.csv")

# Filtros
department = st.sidebar.selectbox("Seleccionar Departamento", data["Department"].unique())

# KPI: Satisfacción promedio
satisfaction = data[data["Department"] == department]["Employee_Satisfaction_Score"].mean()

st.title("Dashboard Interactivo - Wind Telecom")
st.header(f"Departamento: {department}")
st.metric("Satisfacción Promedio", round(satisfaction, 2))

# Gráficos
fig = px.bar(data[data["Department"] == department], x="Employee_ID", y="Productivity", title="Productividad")
st.plotly_chart(fig)
