import streamlit as st
import pandas as pd

# --- GOOGLE SHEETS CONFIG ---
SHEET_ID = "1V2t-o7-6Y_Xh1Ne38DVpUfu_eUrUeJs4AeEuQ9edU6k"

st.set_page_config(page_title="TNSRLM Cloud Tracker", layout="wide")

def load_data_from_google(sheet_name):
    encoded_name = sheet_name.replace(" ", "%20")
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    data = pd.read_csv(url)
    
    # SAFETY: Convert columns to numeric, turning errors like "NA" into 0
    cols_to_fix = ['Target_Units', 'Achieved_Units', 'Budget_Lakhs', 'Expenditure_Lakhs']
    for col in cols_to_fix:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
    
    # Repeat for Income columns if they exist
    if 'Target_Income' in data.columns:
        data['Target_Income'] = pd.to_numeric(data['Target_Income'], errors='coerce').fillna(0)
    if 'Actual_Income' in data.columns:
        data['Actual_Income'] = pd.to_numeric(data['Actual_Income'], errors='coerce').fillna(0)
        
    return data

# --- SCHEMES ---
# Ensure these match your Tab names exactly
schemes = [
    "Cattle Rearing", "Aromatic Plants", "Seed Production", "Backyard Poultry",
    "Goat Rearing", "Quail Rearing", "Spices Cluster", "Cut Flower Cluster",
    "Vegetable Cluster", "Traditional Paddy", "Solar Dryer", "Mushroom Spawn Production",
    "Groundnut Clusters", "Casuarina Cluster", "Incubators", "Vermiworm", "Sericulture"
]

st.sidebar.title("TNSRLM Digital Mission")
selected_scheme = st.sidebar.selectbox("Select Livelihood Cluster", schemes)

try:
    df = load_data_from_google(selected_scheme)
    
    if 'District' in df.columns:
        districts = sorted(df['District'].unique())
        selected_dist = st.sidebar.selectbox("Select District", districts)
        
        row = df[df['District'] == selected_dist].iloc[0]

        st.title(f"📈 {selected_scheme} Progress")
        st.info(f"Viewing live cloud data for {selected_dist}")

        # --- PROGRESS METRICS ---
        col1, col2, col3 = st.columns(3)
        
        t, a = row['Target_Units'], row['Achieved_Units']
        b, e = row['Budget_Lakhs'], row['Expenditure_Lakhs']

        phys_p = (a / t * 100) if t > 0 else 0
        col1.metric("Physical Achievement", f"{int(a)} / {int(t)}", f"{phys_p:.1f}%")
        
        fin_p = (e / b * 100) if b > 0 else 0
        col2.metric("Financial Expenditure", f"Rs.{e:.2f} L", f"of Rs.{b:.2f} L")
        
        col3.metric("Budget Utilization", f"{fin_p:.1f}%")

        # --- INCOME TRACKER ---
        if 'Target_Income' in df.columns and 'Actual_Income' in df.columns:
            st.divider()
            st.subheader("💰 Monthly Income Generation")
            inc1, inc2, inc3 = st.columns(3)
            ti, ai = row['Target_Income'], row['Actual_Income']
            inc_p = (ai / ti * 100) if ti > 0 else 0
            inc1.metric("Income Target", f"Rs.{ti:.2f} L")
            inc2.metric("Income Realized", f"Rs.{ai:.2f} L")
            inc3.metric("Achievement %", f"{inc_p:.1f}%")
        
        st.divider()
        st.write(f"### State-wide Comparison: {selected_scheme}")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error("Column 'District' not found. Please check tab headers.")

except Exception as e:
    st.error(f"Error: {e}")
