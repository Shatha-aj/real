import streamlit as st
import pandas as pd

# --- Custom CSS for background ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #fce4ec);
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #7b1fa2;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏘️ Riyadh Property Neighborhood Recommender")

# Load your real estate dataset
@st.cache_data
def load_data():
    df = pd.read_csv("riyadh.csv")  # <- Replace with your file
    df["Elevator"] = df["Elevator"].astype(str)
    df["Furnished"] = df["Furnished"].astype(str)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Set Your Preferences")

budget = st.sidebar.number_input("Enter your budget (SAR)", min_value=0, step=10000, value=1_000_000)

bedrooms = st.sidebar.selectbox("Bedrooms", sorted(df["Bedrooms"].unique()))
bathrooms = st.sidebar.selectbox("Bathrooms", sorted(df["Bathrooms"].unique()))
floor_number = st.sidebar.selectbox("Floor Number", sorted(df["Floor Number"].unique()))
elevator = st.sidebar.selectbox("Elevator", df["Elevator"].unique())
property_age = st.sidebar.slider("Max Property Age (years)", 0, int(df["Property Age (years)"].max()), 10)
furnished = st.sidebar.selectbox("Furnished", df["Furnished"].unique())

# Button to filter
if st.sidebar.button("Find Neighborhoods"):
    filtered = df[
        (df["Selling Price (SAR)"] <= budget) &
        (df["Bedrooms"] == bedrooms) &
        (df["Bathrooms"] == bathrooms) &
        (df["Floor Number"] == floor_number) &
        (df["Elevator"] == elevator) &
        (df["Property Age (years)"] <= property_age) &
        (df["Furnished"] == furnished)
    ]

   if filtered.empty:
    st.warning("⚠️ No properties match your criteria.")
else:
    st.success("🎯 Top 3 Neighborhoods Matching Your Criteria")

    top_neighs = (
        filtered["Neighborhood"]
        .value_counts()
        .head(3)
        .index.tolist()
    )

    for neigh in top_neighs:
        subset = filtered[filtered["Neighborhood"] == neigh]
        example = subset.head(1).iloc[0]  # Take first matching example

        st.markdown(f"### 🏘️ {neigh}")
        st.markdown(f"- **Region:** {example['Region']}")
        st.markdown(f"- **Area:** {example['Area (sqm)']} sqm")
        st.markdown(f"- **Selling Price:** {example['Selling Price (SAR)']:.0f} SAR")
        st.markdown("---")
else:
    st.info("👉 Set your filters and click 'Find Neighborhoods' to get started.")

  
