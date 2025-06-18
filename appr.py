import streamlit as st
import pandas as pd

# Load your data
@st.cache_data
def load_data():
    df = pd.read_csv("riyadh.csv")  # Replace with your actual file
    return df

df = load_data()

st.title("🏘️ Best Neighborhood Recommender in Riyadh")

# --- Sidebar Inputs ---
st.sidebar.header("Your Preferences")

property_type = st.sidebar.selectbox("Select Property Type", df['Property Type'].unique())
budget = st.sidebar.number_input("Enter Your Budget (SAR)", min_value=50000, max_value=10000000, step=50000)

# --- Filtering Function ---
def recommend_neighborhoods(data, prop_type, max_price):
    filtered = data[
        (data['Property Type'] == prop_type) &
        (data['Selling Price (SAR)'] <= max_price)
    ]
    if filtered.empty:
        return pd.DataFrame()

    grouped = filtered.groupby('Neighborhood').agg(
        Listings=('Selling Price (SAR)', 'count'),
        Median_Price=('Selling Price (SAR)', 'median'),
        Avg_Area=('Area (sqm)', 'mean')
    ).reset_index()

    top = grouped.sort_values(by='Listings', ascending=False).head(3)
    return top

# --- Display Results ---
st.header("📍 Recommended Neighborhoods")
results = recommend_neighborhoods(df, property_type, budget)

if results.empty:
    st.warning("No matching neighborhoods found for this budget and property type.")
else:
    st.dataframe(results.style.format({
        "Median_Price": "SAR {:.0f}",
        "Avg_Area": "{:.1f} sqm"
    }))
