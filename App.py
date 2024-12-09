import streamlit as st
import pandas as pd

# Cargar los datos
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/sjmr0911/Dashboard-Data/refs/heads/main/Extended_Employee_Performance_and_Productivity_Data.csv")

data = load_data()

# Título del dashboard
st.title("Dashboard de KPIs - Wind Telecom")

# Sidebar para filtros
st.sidebar.header("Filtros")
department_filter = st.sidebar.multiselect(
    "Selecciona el Departamento",
    options=data["Department"].unique(),
    default=data["Department"].unique(),
)

# Filtrar los datos
filtered_data = data[data["Department"].isin(department_filter)]

# Cálculo de KPIs
turnover_rate = (filtered_data["Resigned"].sum() / len(filtered_data)) * 100
satisfaction_by_department = filtered_data.groupby("Department")["Employee_Satisfaction_Score"].mean()
productivity_by_department = (
    filtered_data.groupby("Department")
    .apply(lambda x: (x["Projects_Handled"].sum() / x["Work_Hours_Per_Week"].sum()))
)
labor_cost_by_department = filtered_data.groupby("Department")["Monthly_Salary"].sum()
overtime_by_department = filtered_data.groupby("Department")["Overtime_Hours"].mean()

# Mostrar KPIs principales
st.header("KPIs Generales")
st.metric(label="Tasa de Rotación (%)", value=f"{turnover_rate:.2f}")

# Visualizaciones con funciones nativas de Streamlit
st.subheader("Satisfacción Promedio por Departamento")
st.bar_chart(satisfaction_by_department)

st.subheader("Productividad Promedio por Departamento")
st.bar_chart(productivity_by_department)

st.subheader("Costos Laborales Mensuales por Departamento ($USD)")
st.bar_chart(labor_cost_by_department)

st.subheader("Horas Extra Promedio por Departamento")
st.bar_chart(overtime_by_department)
