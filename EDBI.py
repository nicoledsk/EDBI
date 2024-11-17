import streamlit as st
import pandas as pd 
import plotly.express as px
import duckdb

st.title('EDBI Dashboard')

@st.cache_data
def load_data():
    data = pd.read_excel('10768184_EDBI - data exercise_2024_6737201400014F8B0A120001.xlsx', sheet_name='2 - Raw Data', header=5)
    data = pd.DataFrame(data)
    data = data.rename(columns={"Client Identifier": "ClientIdentifier", "Business Division": "BusinessDivision", "Instrument Asset Type": "InstrumentAssetType"} )
    return data

df = load_data()

melted_df = pd.melt(df, id_vars=["ClientIdentifier", "BusinessDivision", "Country", "Region", "Category", "InstrumentAssetType"], var_name="MonthYear", value_name="NumOfDistinctRequests")
melted_df["MonthYear"] = pd.to_datetime(melted_df["MonthYear"], format="%b %Y")  # Ensure proper datetime parsing
with st.expander("Data Preview"):
     st.dataframe(melted_df.head(100), column_config={
          "MonthYear": st.column_config.DatetimeColumn(format= "MMM YYYY"), 
     })
        # Limit 100 rows


if melted_df.empty:
        st.warning("No data available for analysis.")
        @st.cache_data
        def usage_df():
            usage_df = duckdb.sql(
            """
            WITH UsageChange AS (
                SELECT 
                    ClientIdentifier, 
                    MonthYear, 
                    NumOfDistinctRequests AS CurrentMonthRequest, 
                    LAG(NumOfDistinctRequests) 
                        OVER (PARTITION BY ClientIdentifier ORDER BY MonthYear) AS PrevMonthRequest 
                FROM melted_df
            )
            SELECT 
                ClientIdentifier, 
                MonthYear, 
                CurrentMonthRequest, 
                PrevMonthRequest, 
                CASE 
                    WHEN PrevMonthRequest IS NULL THEN 0
                    WHEN CurrentMonthRequest IS NULL THEN 0
                    ELSE CurrentMonthRequest - PrevMonthRequest 
                END AS UsageChange 
            FROM UsageChange 
            ORDER BY ClientIdentifier, MonthYear
            """
            ).df()

            st.dataframe(usage_df.head(100))
            # Limit 100 rows

        

@st.cache_data
def plot_chart(data, chart_type, **kwargs):
    if chart_type == "bar":
        return px.bar(data, **kwargs)
    elif chart_type == "line":
        return px.line(data, **kwargs)

@st.cache_data
def execute_query(query, dataframe):
    try:
        return duckdb.sql(query).df()
    except Exception as e:
        st.error(f"Query execution failed: {e}")
        return pd.DataFrame()

# col_1, col_2, col_3 = st.columns(3)


@st.cache_data
def bd_plot():
    query = """
        SELECT MonthYear, NumOfDistinctRequests, BusinessDivision
        FROM melted_df
    """
    bd_df = execute_query(query, melted_df)
    if not bd_df.empty:
        fig = plot_chart(
            data=bd_df,
            chart_type="bar",
            title="Monthly Requests by Business Division",
            x="MonthYear",
            y="NumOfDistinctRequests",
            color="BusinessDivision"
        )
        st.plotly_chart(fig, use_container_width=True)

bd_plot()

@st.cache_data
def total_plot():
    query = """SELECT SUM(NumofDistinctRequests) AS TotalRequests, MonthYear FROM melted_df GROUP BY MonthYear ORDER BY MonthYear ASC"""
    total_df = execute_query(query, melted_df)
    st.dataframe(total_df.head(100), column_config={
          "MonthYear": st.column_config.DatetimeColumn(format= "MMM YYYY")
          })
total_plot()

@st.cache_data
def client_plot():
    query = """SELECT COUNT(NumOfDistinctRequests) AS TotalCount, ClientIdentifier FROM melted_df GROUP BY ClientIdentifier ORDER BY TotalCount DESC LIMIT 10"""
    client_df = execute_query(query, melted_df)
    st.dataframe(client_df.head(100), column_config={
          "MonthYear": st.column_config.DatetimeColumn(format= "MMM YYYY")
          })

client_plot()

@st.cache_data
def category_plot():
    query = """SELECT MonthYear, NumOfDistinctRequests, Category FROM melted_df"""
    category_df = execute_query(query, melted_df)
    if not category_df.empty:
        fig = plot_chart(data=category_df, chart_type="bar", title="Monthly Requests by Category",
            x="MonthYear",
            y="NumOfDistinctRequests",
            color="Category")
        st.plotly_chart(fig, use_container_width=True)

category_plot()

@st.cache_data
def country_plot():
    query = """
        SELECT MonthYear, NumOfDistinctRequests, Country
        FROM melted_df
    """
    country_df = execute_query(query, melted_df)
    if not country_df.empty:
        fig = plot_chart(
            data=country_df,
            chart_type="line",
            title="Monthly Requests by Country",
            x="MonthYear",
            y="NumOfDistinctRequests",
            color="Country"
        )
        st.plotly_chart(fig, use_container_width=True)

country_plot()

