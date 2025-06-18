import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("riyadh.csv")

df = load_data()

st.title("🏘️ Riyadh Property Neighborhood Recommender")

st.markdown("Get the **top 3 neighborhoods** to buy a property in Riyadh based on your budget and preferred property type.")

# Sidebar user input
st.sidebar.header("🔍 Filter Options")

# Select box for property type
property_types = df["Property Type"].dropna().unique().tolist()
selected_type = st.sidebar.selectbox("Choose Property Type", sorted(property_types))

# Slider for budget
min_price = int(df["Selling Price (SAR)"].min())
max_price = int(df["Selling Price (SAR)"].max())
selected_budget = st.sidebar.slider("Set your budget (SAR)", min_price, max_price, 1000000, step=50000)

# Filter the data
filtered = df[
    (df["Property Type"] == selected_type) &
    (df["Selling Price (SAR)"] <= selected_budget)
]

# Show results
st.subheader(f"Top 3 Neighborhoods for a '{selected_type}' under {selected_budget:,.0f} SAR")

if filtered.empty:
    st.warning("❌ No matching properties found. Try increasing your budget or changing property type.")
else:
    top_neigh = (
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
        top_neigh.style.format({
            "Median_Price": "SAR {:.0f}",
            "Avg_Area": "{:.1f} sqm"
        })
    )
