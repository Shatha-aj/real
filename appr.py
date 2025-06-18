import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("riyadh.csv")

df = load_data()

st.title("🏘️ Riyadh Property Neighborhood Recommender")

st.markdown("Use the filters below, then click the button to get the top 3 neighborhoods that match your preferences.")

# Sidebar filters
st.sidebar.header("🔍 Search Filters")

# Budget slider
min_price = int(df["Selling Price (SAR)"].min())
max_price = int(df["Selling Price (SAR)"].max())
budget = st.sidebar.slider("Budget (SAR)", min_price, max_price, 1_000_000, step=50_000)

# Bedrooms selectbox
bedrooms = st.sidebar.selectbox("Bedrooms", sorted(df["Bedrooms"].dropna().unique()))

# Bathrooms selectbox
bathrooms = st.sidebar.selectbox("Bathrooms", sorted(df["Bathrooms"].dropna().unique()))

# Floor Number slider
floor_number = st.sidebar.slider("Floor Number", int(df["Floor Number"].min()), int(df["Floor Number"].max()), 0)

# Elevator selectbox
elevator = st.sidebar.selectbox("Elevator", df["Elevator"].dropna().unique().tolist())

# Property Age slider
property_age = st.sidebar.slider("Max Property Age (years)", int(df["Property Age (years)"].min()), int(df["Property Age (years)"].max()), 10)

# Furnished selectbox
furnished = st.sidebar.selectbox("Furnished", df["Furnished"].dropna().unique().tolist())

# Button to trigger search
if st.sidebar.button("🔎 Find Neighborhoods"):

    # Filter based on all inputs
    filtered = df[
        (df["Selling Price (SAR)"] <= budget) &
        (df["Bedrooms"] == bedrooms) &
        (df["Bathrooms"] == bathrooms) &
        (df["Floor Number"] == floor_number) &
        (df["Elevator"] == elevator) &
        (df["Property Age (years)"] <= property_age) &
        (df["Furnished"] == furnished)
    ]

    st.subheader(f"Top 3 Neighborhoods for Your Criteria")

    if filtered.empty:
        st.warning("❌ No matching properties found. Try adjusting your filters.")
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
else:
    st.info("👈 Set your filters and click 'Find Neighborhoods' to get started.")
