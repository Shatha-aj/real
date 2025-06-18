import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("riyadh.csv")

df = load_data()

st.title("🏘️ Riyadh Property Recommender")

# Sidebar input
st.sidebar.header("Search Criteria")
prop_type = st.sidebar.selectbox("Property Type", df['Property Type'].unique())
budget = st.sidebar.number_input("Max Budget (SAR)", value=1000000, step=50000)

# Filter & recommend
filtered = df[(df['Property Type'] == prop_type) & (df['Selling Price (SAR)'] <= budget)]

if filtered.empty:
    st.warning("No matching properties found.")
else:
    top3 = (filtered.groupby('Neighborhood')
                    .agg(Listings=('Selling Price (SAR)', 'count'),
                         Median_Price=('Selling Price (SAR)', 'median'),
                         Avg_Area=('Area (sqm)', 'mean'))
                    .sort_values(by='Listings', ascending=False)
                    .head(3)
                    .reset_index())
    
    st.success("Top 3 Neighborhoods:")
    st.dataframe(top3.style.format({"Median_Price": "SAR {:.0f}", "Avg_Area": "{:.1f} sqm"}))
