import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
@st.cache
def load_data():
    return pd.read_csv("https://github.com/sjmr0911/Dashboard-Data/blob/main/Extended_Employee_Performance_and_Productivity_Data.csv")

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

# Visualizaciones
st.subheader("Satisfacción Promedio por Departamento")
fig = px.bar(
    satisfaction_by_department,
    x=satisfaction_by_department.index,
    y=satisfaction_by_department.values,
    labels={"x": "Departamento", "y": "Puntaje Promedio de Satisfacción"},
    title="Satisfacción Promedio por Departamento",
)
st.plotly_chart(fig)

st.subheader("Productividad Promedio por Departamento")
fig = px.bar(
    productivity_by_department,
    x=productivity_by_department.index,
    y=productivity_by_department.values,
    labels={"x": "Departamento", "y": "Proyectos/Hora Trabajada"},
    title="Productividad Promedio por Departamento",
)
st.plotly_chart(fig)

st.subheader("Costos Laborales Mensuales por Departamento ($USD)")
fig = px.bar(
    labor_cost_by_department,
    x=labor_cost_by_department.index,
    y=labor_cost_by_department.values,
    labels={"x": "Departamento", "y": "Costos ($USD)"},
    title="Costos Laborales Mensuales por Departamento",
)
st.plotly_chart(fig)

st.subheader("Horas Extra Promedio por Departamento")
fig = px.bar(
    overtime_by_department,
    x=overtime_by_department.index,
    y=overtime_by_department.values,
    labels={"x": "Departamento", "y": "Horas Promedio"},
    title="Horas Extra Promedio por Departamento",
)
st.plotly_chart(fig)
