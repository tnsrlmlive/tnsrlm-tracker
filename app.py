import streamlit as st
import pandas as pd

# 1. THE MASTER LIST - Add all your 17 GIDs here as you create them
SCHEME_CONFIG = {
    "Backyard Poultry": {
        "gid": "1866299669",
        "highlights": ["Chicks procured", "Total chicks survived", "Chicks Survived During the month", "Target Income", "Income during the month"]
    },
    "Goat Rearing": {
        "gid": "1747779727",
        "highlights": ["Total Goats captured in Muzzle App", "Premium paid Goats Total"]
    },
    
    "Quail Rearing": {
        "gid": "920866231",
        "highlights": ["Quail chicks procured Total", "Quails sold Total", "Income during the month", "Incubator Procured Total" ]
    },
    "Cattle Rearing": {
        "gid": "1651367216",
        "highlights": ["Total Cows captured in Muzzle App", "Premium paid Cows Total", "Quantity of Milk Sold (in Lit) Total", "Income (in Rs.) during the month", "Clusters submitted proposal Total", "Clusters Procured Value addition Machinary Total" ]
    },
    "Sericulture": {
        "gid": "491914730",
        "highlights": ["Cocoon sold (Kg) Total", "Income during the month" ]
    },
    "Vermiworm": {
        "gid": "355607944",
        "highlights": ["Income during the month" ]
    },
    "Incubators": {
        "gid": "2070816617",
        "highlights": ["Chicks hatched and sold Total", "Target Income", "Income during the month" ]
    },
    "Aromatic Plants": {
        "gid": "109971273",
        "highlights": ["procured Value addition machinery Total", "Target Income", "Income during the month" ]
    },
    "Casuarina Cluster": {
        "gid": "1577560532",
        "highlights": ["Profile submitted", "UC Submitted" ]
    },
    "Mushroom Spawn": {
        "gid": "52247309",
        "highlights": ["Machineries Procurement completed", "Machinery Installed", "Production Started", "Target Income", "Income during the month" ]
    },
    "Solar Dryer": {
        "gid": "2082147746",
        "highlights": ["Clusters procured", "Fund release", "Produce dried", "Income" ]
    },
    "Groundnut Clusters": {
        "gid": "1376425211",
        "highlights": ["machinery", "Value addition", "Income", "Fund release", "to Cluster", "Beneficiaries" ]
    },
    "Spices Cluster": {
        "gid": "34261868",
        "highlights": ["Machinery procured", "Income" ]
    },
    "Seed Production": {
        "gid": "1343554782",
        "highlights": ["harvesting", "TANSEDA", "Income" ]
    },
    "Cut Flower": {
        "gid": "251319955",
        "highlights": ["Poly houses", "Micro Irrigation", "planting", "Fund released" ]
    },
     "Vegetable Cluster": {
        "gid": "1677063468",
        "highlights": ["Income", "procured machinery", "Fund released" ]
    },
    "Traditional Paddy": {
        "gid": "633846517",
        "highlights": ["Income", "proposal", "procured machinery" ]
    },# Add your other 15 schemes here following the same format
    # "Milk Processing": {"gid": "GID_NUMBER", "highlights": ["Liters", "Fat", "Value"]},
}

st.set_page_config(page_title="TNSRLM Multi-Scheme Dashboard", layout="wide")

# This function ensures we get fresh data for the specific tab only
@st.cache_data(ttl=60) # Refreshes every minute
def load_tab_data(gid):
    SHEET_ID = '1V2t-o7-6Y_Xh1Ne38DVpUfu_eUrUeJs4AeEuQ9edU6k'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}'
    # We use keep_default_na=False to prevent 'nan' from appearing
    data = pd.read_csv(url, keep_default_na=False)
    return data

# --- SIDEBAR ---
st.sidebar.header("📋 MIS Filter Options")
selected_scheme = st.sidebar.selectbox("1. Select Scheme", list(SCHEME_CONFIG.keys()))

try:
    # Load ONLY the data for the selected scheme tab
    conf = SCHEME_CONFIG[selected_scheme]
    df = load_tab_data(conf['gid'])

    # Find District Column (Smart Finder)
    dist_col = next((c for c in df.columns if 'District' in c), None)

    if dist_col:
        # Clean the list of Districts
        dist_list = sorted([str(x).strip() for x in df[dist_col].unique() if str(x).strip() not in ['', '0', 'Select District']])
        selected_district = st.sidebar.selectbox("2. Select District", dist_list)
        
        # FILTER: This ensures the table ONLY shows the specific District for this specific Scheme
        final_df = df[df[dist_col].astype(str).str.strip() == selected_district]

        # --- DASHBOARD DISPLAY ---
        st.title(f"📊 {selected_scheme}")
        st.info(f"Viewing abstract for: **{selected_district}**")

        # --- HIGHLIGHT CARDS ---
        st.subheader(f"📍 Key Performance Indicators")
        metrics = st.columns(3)
        
        for i, keyword in enumerate(conf['highlights']):
            with metrics[i % 3]:
                # Find the column that contains the keyword
                col_name = next((c for c in final_df.columns if keyword.lower() in c.lower()), None)
                if col_name and not final_df.empty:
                    val = final_df[col_name].iloc[0]
                    st.metric(label=col_name, value=val)
                else:
                    st.metric(label=keyword, value="0")

        st.divider()

        # --- FULL SCHEME TABLE ---
        st.subheader(f"📑 Complete {selected_scheme} Data: {selected_district}")
        # We display the filtered data which is guaranteed to be from the selected tab
        st.dataframe(final_df, use_container_width=True)

    else:
        st.error(f"The tab for {selected_scheme} does not have a 'District' column.")

except Exception as e:
    st.error(f"Connection Error: {e}")
