import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("riyadh.csv")
    return df

df = load_data()

st.title("🏘️ Riyadh Neighborhood Recommender")

# --- Sidebar User Input ---
st.sidebar.header("Search Filters")

# Property type selection
property_types = df["Property Type"].dropna().unique()
selected_type = st.sidebar.selectbox("Choose Property Type", sorted(property_types))

# Budget input
budget = st.sidebar.number_input("Enter your budget (SAR)", min_value=50000, step=50000, value=1000000)

# --- Filter data ---
filtered_df = df[
    (df["Property Type"] == selected_type) &
    (df["Selling Price (SAR)"] <= budget)
]

st.subheader(f"Top 3 Neighborhoods to buy a '{selected_type}' under {budget:,.0f} SAR")

if filtered_df.empty:
    st.warning("No matching properties found. Try increasing the budget or changing property type.")
else:
    # Group by neighborhood and summarize
    top_neighborhoods = (
        filtered_df.groupby("Neighborhood")
        .agg(
            Listings=('Selling Price (SAR)', 'count'),
            Median_Price=('Selling Price (SAR)', 'median'),
            Avg_Area=('Area (sqm)', 'mean')
        )
        .sort_values(by="Listings", ascending=False)
        .head(3)
        .reset_index()
    )

    # Format and display result
    st.dataframe(
        top_neighborhoods.style.format({
            "Median_Price": "SAR {:.0f}",
            "Avg_Area": "{:.1f} sqm"
        })
    )

    
