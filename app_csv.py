"""
Simple CSV-Based Propeller Optimizer Web App
No complex calculations - just CSV file lookup!
Works without numpy, scipy, matplotlib!
"""

import streamlit as st
import csv
from pathlib import Path

# Page config
st.set_page_config(
    page_title="CSV Propeller Optimizer",
    page_icon="🚢",
    layout="wide"
)

# Title
st.title("🚢 CSV-Based Propeller Optimizer")
st.subheader("Simple database lookup - No complex calculations needed!")

# Load CSV database
@st.cache_data
def load_propeller_database():
    """Load propeller database from CSV"""
    db_file = Path('data/propeller_database.csv')
    if not db_file.exists():
        return []

    with open(db_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

@st.cache_data
def load_speed_ranges():
    """Load speed ranges from CSV"""
    file = Path('data/speed_ranges.csv')
    if not file.exists():
        return []

    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Load data
propeller_db = load_propeller_database()
speed_ranges = load_speed_ranges()

if not propeller_db:
    st.error("⚠️ Database not found! Please ensure data/propeller_database.csv exists")
    st.stop()

st.success(f"✅ Loaded {len(propeller_db)} vessels from database")

# Sidebar
st.sidebar.header("📋 Vessel Parameters")

# Show available vessels
st.sidebar.subheader("Quick Select Vessel:")
vessel_names = [v['vessel_type'].replace('_', ' ').title() for v in propeller_db]
selected_vessel = st.sidebar.selectbox("Choose from database:", ["Custom"] + vessel_names)

if selected_vessel != "Custom":
    # Find selected vessel
    vessel_data = None
    for v in propeller_db:
        if v['vessel_type'].replace('_', ' ').title() == selected_vessel:
            vessel_data = v
            break

    if vessel_data:
        speed = float(vessel_data['speed_knots'])
        displacement = float(vessel_data['displacement_tons'])
        draft = float(vessel_data['draft_m'])
    else:
        speed = 30.0
        displacement = 10.0
        draft = 0.8
else:
    speed = 30.0
    displacement = 10.0
    draft = 0.8

# Input parameters
st.sidebar.subheader("Or Enter Custom Values:")
speed = st.sidebar.slider("Speed (knots)", 10.0, 80.0, speed, 1.0)
displacement = st.sidebar.number_input("Displacement (tons)", 1.0, 50.0, displacement, 0.5)
draft = st.sidebar.number_input("Draft (m)", 0.3, 3.0, draft, 0.1)

# Find button
if st.sidebar.button("🔍 FIND PROPELLER", type="primary"):
    st.session_state.search_done = True
else:
    st.session_state.search_done = False

# Main content
if st.session_state.get('search_done', False):
    st.markdown("---")
    st.subheader("🎯 Search Results")

    # Find similar vessel
    best_match = None
    min_diff = float('inf')

    for vessel in propeller_db:
        speed_diff = abs(float(vessel['speed_knots']) - speed)
        disp_diff = abs(float(vessel['displacement_tons']) - displacement)
        draft_diff = abs(float(vessel['draft_m']) - draft)

        difference = speed_diff * 2.0 + disp_diff * 1.0 + draft_diff * 3.0

        if difference < min_diff:
            min_diff = difference
            best_match = vessel

    if best_match:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Match Found", best_match['vessel_type'].replace('_', ' ').title())
            st.metric("Match Quality", "Excellent" if min_diff < 5 else "Good")

        with col2:
            st.metric("Database Speed", f"{best_match['speed_knots']} knots")
            st.metric("Your Speed", f"{speed:.1f} knots")

        with col3:
            st.metric("Database Displacement", f"{best_match['displacement_tons']} tons")
            st.metric("Your Displacement", f"{displacement:.1f} tons")

        st.markdown("---")
        st.subheader("📊 Propeller Specifications")

        # Results in columns
        col_a, col_b, col_c, col_d, col_e = st.columns(5)

        with col_a:
            diameter_m = float(best_match['diameter_m'])
            st.metric("Diameter", f"{diameter_m:.2f} m",
                     f"{diameter_m * 39.37:.1f} inches")

        with col_b:
            st.metric("Pitch Ratio", f"{best_match['pitch_ratio']}")

        with col_c:
            efficiency = float(best_match['efficiency'])
            st.metric("Efficiency", f"{efficiency:.3f}",
                     f"{efficiency*100:.1f}%")

        with col_d:
            st.metric("Blade Count", best_match['blade_count'])

        with col_e:
            st.metric("Material", best_match['material'].title())

        # Additional info
        st.markdown("---")
        st.subheader("📝 Additional Information")

        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.write("**Performance Data:**")
            st.write(f"- KT (Thrust Coefficient): {best_match['kt']}")
            st.write(f"- KQ (Torque Coefficient): {best_match['kq']}")
            st.write(f"- RPM: {best_match['rpm']}")
            st.write(f"- Power: {best_match['power_kw']} kW")

        with info_col2:
            st.write("**Design Notes:**")
            st.info(best_match['notes'])

        # Speed category
        speed_cat = None
        for cat in speed_ranges:
            if float(cat['min_speed']) <= speed <= float(cat['max_speed']):
                speed_cat = cat
                break

        if speed_cat:
            st.markdown("---")
            st.subheader("⚡ Speed Category Analysis")

            cat_col1, cat_col2, cat_col3 = st.columns(3)

            with cat_col1:
                st.write(f"**Category:** {speed_cat['speed_category'].replace('_', ' ').title()}")
                st.write(f"**Speed Range:** {speed_cat['min_speed']}-{speed_cat['max_speed']} knots")

            with cat_col2:
                st.write(f"**Propeller Type:** {speed_cat['propeller_type']}")
                st.write(f"**Cavitation Risk:** {speed_cat['cavitation_risk']}")

            with cat_col3:
                st.write(f"**Recommended Pitch Ratio:** {speed_cat['recommended_pitch_ratio']}")
                st.write(f"**Recommended Blades:** {speed_cat['recommended_blade_count']}")

        # Download result
        st.markdown("---")
        st.subheader("💾 Export Results")

        result_text = f"""PROPELLER DESIGN REPORT
========================

Input Parameters:
-----------------
Speed:          {speed:.1f} knots
Displacement:   {displacement:.1f} tons
Draft:          {draft:.2f} m

Matched Vessel:
---------------
Type:           {best_match['vessel_type'].replace('_', ' ').title()}
Match Quality:  {"Excellent" if min_diff < 5 else "Good"}

Propeller Specifications:
-------------------------
Diameter:       {best_match['diameter_m']} m ({float(best_match['diameter_m']) * 39.37:.1f} inches)
Pitch Ratio:    {best_match['pitch_ratio']}
Efficiency:     {best_match['efficiency']} ({float(best_match['efficiency'])*100:.1f}%)
Blade Count:    {best_match['blade_count']}
Material:       {best_match['material']}

Performance:
-----------
KT:             {best_match['kt']}
KQ:             {best_match['kq']}
RPM:            {best_match['rpm']}
Power:          {best_match['power_kw']} kW

Notes: {best_match['notes']}

Source: CSV Database
Generated by CSV Propeller Optimizer
"""

        st.download_button(
            label="📄 Download Report",
            data=result_text,
            file_name=f"propeller_design_{speed:.0f}knots.txt",
            mime="text/plain"
        )

else:
    # Welcome screen
    st.info("👈 Select a vessel from the sidebar or enter custom parameters, then click 'FIND PROPELLER'")

    st.markdown("---")
    st.subheader("📚 Available Vessels in Database")

    # Show database as table
    import pandas as pd

    # Convert to display format
    display_data = []
    for v in propeller_db:
        display_data.append({
            'Vessel Type': v['vessel_type'].replace('_', ' ').title(),
            'Speed (knots)': v['speed_knots'],
            'Displacement (tons)': v['displacement_tons'],
            'Diameter (m)': v['diameter_m'],
            'Efficiency': f"{float(v['efficiency'])*100:.1f}%",
            'Material': v['material'].title()
        })

    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("💡 How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 1️⃣ Simple Database
        All propeller designs stored in CSV files
        - Easy to edit
        - No complex calculations
        - Fast lookups
        """)

    with col2:
        st.markdown("""
        ### 2️⃣ Smart Matching
        Finds most similar vessel
        - Speed matching
        - Displacement matching
        - Draft matching
        """)

    with col3:
        st.markdown("""
        ### 3️⃣ Instant Results
        Get specifications immediately
        - No waiting
        - No installation needed
        - Works in browser
        """)

# Footer
st.markdown("---")
st.caption("🌊 CSV-Based Propeller Optimizer | No complex dependencies needed! | Open Source")
