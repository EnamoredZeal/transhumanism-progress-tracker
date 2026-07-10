import json
import os
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Transhumanism Progress Tracker",
    page_icon="🧬",
    layout="wide"
)

# 1. Main Title Header
st.title("Transhumanism Progress Tracker")
st.subheader("An empirical index monitoring the convergence of biology, hardware, and consciousness.")

# 2. Prominent Epistemic Humility Banner (Friction Point for Safety)
with st.expander("📖 READ FIRST: Methodology, Risk, & Epistemic Humility", expanded=True):
    st.markdown("""
    ### Welcome to the first empirical Transhumanism Tracker.
    Because this index monitors highly experimental, cutting-edge technologies, we carry a strict responsibility to prevent information bias, premature speculation, and unsafe real-world behaviors.
    
    * **No Hype:** This dashboard is not a countdown clock. It is an objective ledger of peer-reviewed engineering milestones.
    * **The TRL Gate:** Every metric is bound to a strict **Technology Readiness Level (TRL)** from 1 to 9. If a breakthrough has not cleared human clinical trials (TRL 6+), it is explicitly flagged as **Pre-Clinical**.
    * **No Self-Experimentation:** Early-stage metrics (TRL 1-5) are highly experimental. Attempting to replicate laboratory or animal-stage protocols outside of controlled medical settings is exceptionally dangerous.
    
    *If you are a researcher and spot an error or want to contribute peer-reviewed data, please submit an issue or pull request on our [GitHub Repository](https://github.com/EnamoredZeal/transhumanism-progress-tracker).*
    """)

st.markdown("---")

# 3. Data Loading Pipeline
@st.cache_data
def load_tracker_data():
    # Looks for database file in the relative project path
    db_path = os.path.join("core", "database.json")
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            return json.load(f)
    return None

data = load_tracker_data()

if not data:
    st.error("⚠️ Error: 'core/database.json' not found. Please ensure the file is initialized in your GitHub repository.")
else:
    # 4. Top-level Metadata Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="System Status", value="Operational / Verified")
    with col2:
        # Formats the raw timestamp to a clean date
        raw_date = data.get("last_updated", "N/A")
        clean_date = raw_date.split("T")[0] if "T" in raw_date else raw_date
        st.metric(label="Last Database Update", value=clean_date)
    with col3:
        st.metric(label="Tracking Pillars", value="4 Convergent Fields")

    st.markdown("---")

    # 5. Interactive Pillar Exploration
    st.header("📊 Convergent Field Metrics")
    
    pillar_selection = st.selectbox(
        "Select a pillar to view its empirical milestones:",
        [
            "Cybernetic Integration (BCIs & Neurotech)",
            "Genetic & Cellular Modification",
            "Somatic Augmentation (Hardware & Organs)",
            "Cognitive & Consciousness Sciences"
        ]
    )

    # Helper function to parse metric arrays into displayable rows
    def compile_metrics_table(pillar_data):
        rows = []
        for metric_name, entries in pillar_data.items():
            if not entries:
                # Placeholder for empty metrics
                rows.append({
                    "Metric": metric_name.replace("_", " ").title(),
                    "Current Value": "No verified data logged yet",
                    "TRL": "N/A",
                    "Tested on Humans": "N/A",
                    "Safety Status / Warning": "N/A",
                    "Citation Source": "N/A"
                })
            else:
                for entry in entries:
                    rows.append({
                        "Metric": metric_name.replace("_", " ").title(),
                        "Current Value": f"{entry['value']} {entry['unit']}",
                        "TRL": f"TRL {entry['trl_level']}",
                        "Tested on Humans": "Yes" if entry["is_human_tested"] else "No (Animal/In-Vitro)",
                        "Safety Status / Warning": entry["safety_status"],
                        "Citation Source": entry["source_citation"]
                    })
        return pd.DataFrame(rows)

    # Route UI display based on dropdown selection
    if "Cybernetic" in pillar_selection:
        st.write("### Cybernetic Integration Metrics")
        df = compile_metrics_table(data.get("cybernetic_integration", {}))
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif "Genetic" in pillar_selection:
        st.write("### Genetic & Cellular Modification Metrics")
        df = compile_metrics_table(data.get("genetic_cellular_modification", {}))
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif "Somatic" in pillar_selection:
        st.write("### Somatic Augmentation Metrics")
        df = compile_metrics_table(data.get("somatic_augmentation", {}))
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif "Cognitive" in pillar_selection:
        st.write("### Cognitive & Consciousness Sciences Metrics")
        df = compile_metrics_table(data.get("cognitive_consciousness_sciences", {}))
        st.dataframe(df, use_container_width=True, hide_index=True)
