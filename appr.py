import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("riyadh.csv")

df = load_data()

st.title("🏘️ Riyadh Property Neighborhood Recommender")

st.markdown("""
Use the filters below to find the top 3 neighborhoods matching your preferences.
""")

# Sidebar filters
st.sidebar.header("🔍 Search Filters")

# Budget slider
min_price = int(df["Selling Price (SAR)"].min())
max_price = int(df["Selling Price (SAR)"].max())
budget = st.sidebar.slider("Budget (SAR)", min_price, max_price, 1_000_000, step=50_000)

# Bedrooms selectbox
bedroom_options = sorted(df["Bedrooms"].dropna().unique())
bedrooms = st.sidebar.selectbox("Bedrooms", bedroom_options)

# Bathrooms selectbox
bathroom_options = sorted(df["Bathrooms"].dropna().unique())
bathrooms = st.sidebar.selectbox("Bathrooms", bathroom_options)

# Floor Number slider (assumes floor numbers start from 0 or 1)
min_floor = int(df["Floor Number"].min())
max_floor = int(df["Floor Number"].max())
floor_number = st.sidebar.slider("Floor Number", min_floor, max_floor, min_floor)

# Elevator selectbox
elevator_options = df["Elevator"].dropna().unique().tolist()
elevator = st.sidebar.selectbox("Elevator", elevator_options)

# Property Age slider
min_age = int(df["Property Age (years)"].min())
max_age = int(df["Property Age (years)"].max())
property_age = st.sidebar.slider("Max Property Age (years)", min_age, max_age, max_age)

# Furnished selectbox
furnished_options = df["Furnished"].dropna().unique().tolist()
furnished = st.sidebar.selectbox("Furnished", furnished_options)

# Filter the dataframe based on user input
filtered = df[
    (df["Selling Price (SAR)"] <= budget) &
    (df["Bedrooms"] == bedrooms) &
    (df["Bathrooms"] == bathrooms) &
    (df["Floor Number"] == floor_number) &
    (df["Elevator"] == elevator) &
    (df["Property Age (years)"] <= property_age) &
    (df["Furnished"] == furnished)
]

st.subheader(f"Top 3 Neighborhoods matching your criteria")

if filtered.empty:
    st.warning("No properties found matching your filters. Try adjusting them.")
else:
    top_neighborhoods = (
        filtered.groupby("Neighborhood")
        .agg(
            Listings=('Selling Price (SAR)', 'count'),
            Median_Price=('Selling Price (SAR)', 'median'),
            Avg_Area=('Area (sqm)', 'mean')
        )
        .sort_values(by="Listings", ascending=False)
        .head(3)
        .reset_index()
    )

    st.dataframe(
        top_neighborhoods.style.format({
            "Median_Price": "SAR {:.0f}",
            "Avg_Area": "{:.1f} sqm"
        })
    )
