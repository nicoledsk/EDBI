import streamlit as st 
import pandas as pd 
import plotly.express as px

st.title('EDBI Dashboard')

@st.cache_data
def load_data():
    data = pd.read_excel("10768184_EDBI - data exercise_2024_6737201400014F8B0A120001.xlsx", sheet_name='2 - Raw Data', header=5)
    return data

df = load_data()
melted_df = pd.melt(df, id_vars=["Client Identifier", "Business Division", "Country", "Region", "Category", "Instrument Asset Type"], var_name="MonthYear", value_name="Number of distinct requests")
with st.expander("Data Preview"):
     st.dataframe(melted_df)

# col_1, col_2, col_3 = st.columns(3)

fig = px.bar(melted_df, x="MonthYear", y="Number of distinct requests", color="Business Division")
st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(melted_df, x="Country", y="Number of distinct requests", color="Country")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(melted_df, x="MonthYear", y="Number of distinct requests", color="Category")
st.plotly_chart(fig2, use_container_width=True)