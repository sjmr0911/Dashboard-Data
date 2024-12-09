import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
fig, ax = plt.subplots()
satisfaction_by_department.plot(kind="bar", color="teal", alpha=0.7, ax=ax)
ax.set_ylabel("Puntaje Promedio de Satisfacción")
ax.set_xlabel("Departamento")
ax.set_title("Satisfacción Promedio por Departamento")
st.pyplot(fig)

st.subheader("Productividad Promedio por Departamento")
fig, ax = plt.subplots()
productivity_by_department.plot(kind="bar", color="orange", alpha=0.7, ax=ax)
ax.set_ylabel("Proyectos/Hora Trabajada")
ax.set_xlabel("Departamento")
ax.set_title("Productividad Promedio por Departamento")
st.pyplot(fig)

st.subheader("Costos Laborales Mensuales por Departamento ($USD)")
fig, ax = plt.subplots()
labor_cost_by_department.plot(kind="bar", color="green", alpha=0.7, ax=ax)
ax.set_ylabel("Costos ($USD)")
ax.set_xlabel("Departamento")
ax.set_title("Costos Laborales Mensuales por Departamento")
st.pyplot(fig)

st.subheader("Horas Extra Promedio por Departamento")
fig, ax = plt.subplots()
overtime_by_department.plot(kind="bar", color="purple", alpha=0.7, ax=ax)
ax.set_ylabel("Horas Promedio")
ax.set_xlabel("Departamento")
ax.set_title("Horas Extra Promedio por Departamento")
st.pyplot(fig)
