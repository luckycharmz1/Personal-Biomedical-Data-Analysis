# =========================
# Imports
# =========================
from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Biomedical Dashboard",
    layout="wide"
)


# =========================
# Sidebar Navigation
# =========================
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=[
            "Home",
            "Data Viewer",
            "Graphs",
            "Research Background & Credentials",
            "Contact"
        ],
        icons=[
            "house",
            "file-earmark-text",
            "bar-chart",
            "mortarboard",
            "envelope"
        ],
        menu_icon="cast",
        default_index=0
    )


# =========================
# Data Folder
# =========================
data_folder = Path("Samsung Health")  # folder containing CSVs

# =========================
# HOME PAGE
# =========================
if selected == "Home":
    st.title("Charmaine's Biomedical Data Dashboard")

    st.markdown(
        """
        Welcome to my biomedical data exploration dashboard.

        This project bridges science and technology, combining my love
        for data with my lived experience with sickle cell anemia.

        From September 2025 to December 2025, I worked with a Stanford University
        mentor to develop hypotheses about physiological patterns that may
        precede sickle cell crises.

        I have then to go on to conduct my own independent research on wearable 
        technology and sickle cell anemia. I greatly appreciate my mentor Dr. Nowah Afangbedii
        for giving me the knowleedge to conduct this independent research. 

        This dashboard explores trends in wearable data to identify
        meaningful patterns over time.

        ⚠️ This tool is exploratory and not intended for medical diagnosis.
        """
    )

    st.markdown("---")
    st.info("This is an evolving research and portfolio project.")
    st.markdown(
        """
        Here is the unofficial scientific research paper. 
        Currently, its only contents consists of the Obersavation and Hypothesis as of now. As it
        is not a completed experiment.
        
        Click here to read: "[Charmaine's Unofficial Scientific Research Paper](https://docs.google.com/document/d/1v469ivc47A7XoQT55V1xtfQh5k40MWHi3-0tb7b99n0/edit?usp=sharing)"
        """
    )



# =========================
# RESEARCH BACKGROUND & CREDENTIALS
# =========================
elif selected == "Research Background & Credentials":
    st.title("Research Background & Credentials")

    st.write(
        "This page highlights my research experience, academic "
        "development, and training in biomedical data analysis."
    )

    st.divider()

    # Stanford University Science Small Group
    st.subheader("Research Experience")

    st.markdown("### Stanford University Science Small Group")
    st.caption("September–December 2025")

    st.write(
        "Participated in a 4 month research program learning and hypothesis development, "
        "exploring potential physiological patterns related to "
        "sickle cell disease."
    )

    stanford_certificate = (
        Path("pictures") /
        "ssg.png"
    )

    if stanford_certificate.exists():
        st.image(
            str(stanford_certificate),
            caption="Stanford University Science Small Group — Certificate of Completion",
            width=500
        )
    else:
        st.warning(
            f"Certificate image not found: {stanford_certificate}"
        )

    st.markdown("### Stanford University Internship")
    st.caption("May–August 2024")

    st.write(
        "Gained exposure to scientific research involving Lyme disease "
        "and E. coli."
    )

    st.divider()

    # Python certificate
    st.subheader("Relevant Coursework & Training")

    st.markdown("### Python for Health Sciences and Healthcare")
    st.caption("Completed — October 2026")

    st.write(
        "Completed training in Python applications relevant to "
        "health sciences and healthcare data analysis."
    )

    python_certificate = (
        Path("pictures") / "linkedin_certificate.jpeg"
    )

    if python_certificate.exists():
        st.image(
            str(python_certificate),
            caption="Python for Health Sciences and Healthcare — Certificate",
            width=500
        )
    else:
        st.warning(
            f"Certificate image not found: {python_certificate}"
        )

    st.markdown(
        "### Biology Meets Programming: Bioinformatics for Beginners"
    )
    st.caption("University of California San Diego — In progress")

    st.divider()

    # Current project
    st.subheader("Independent Project")

    st.markdown("### Personal Biomedical Data Analysis Dashboard")

    st.write(
        "Developing a Python and Streamlit application to explore "
        "historical Samsung Health data and investigate potential "
        "relationships between wearable measurements, lifestyle "
        "factors, and recorded symptoms."
    )

    st.info(
        "This is an exploratory research project and is not intended "
        "to diagnose medical conditions or predict sickle cell crises."
    )


# =========================
# GRAPHS PAGE
# =========================
elif selected == "Graphs":
    st.header("Interactive Biomedical Graphs")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder '{data_folder}' does not exist.")
    else:
        all_files = [f for f in data_folder.glob("*.csv") if f.is_file()]

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            # Dropdown menu for CSV selection
            selected_file = st.selectbox(
                "Select dataset to visualize",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                # Read CSV without headers
                df = pd.read_csv(selected_file, header=None, engine="python", on_bad_lines="skip")

                if df.empty:
                    st.warning("CSV file is empty.")
                else:
                    # Single-column CSV
                    if df.shape[1] == 1:
                        col_name = selected_file.stem
                        df_numeric = pd.to_numeric(df[0], errors="coerce")
                        st.subheader(f"{col_name}")

                        fig = px.line(
                            df_numeric,
                            y=df_numeric,
                            labels={"y": col_name, "index": "Index"},
                            title=col_name
                        )
                        fig.update_traces(line=dict(color="purple"))
                        st.plotly_chart(fig, use_container_width=True)

                    # Multi-column CSV
                    else:
                        df_numeric = pd.DataFrame()
                        for i, col in enumerate(df.columns):
                            col_name = f"{selected_file.stem}_col{i+1}"
                            temp_col = df[col].astype(str).str.replace(r"[^0-9.-]", "", regex=True)
                            df_numeric[col_name] = pd.to_numeric(temp_col, errors="coerce")

                        metric = st.selectbox(
                            "Select metric to analyze",
                            df_numeric.columns
                        )
                        st.subheader(f"{metric}")

                        fig = px.line(
                            df_numeric,
                            y=metric,
                            labels={"y": metric, "index": "Index"},
                            title=metric
                        )
                        fig.update_traces(line=dict(color="purple"))
                        st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error processing {selected_file.name}: {e}")

# =========================
# CONTACT PAGE
# =========================
elif selected == "Contact":
    st.header("Contact")

    st.markdown(
        "🌐 Connect with me here: "
        "[Charmaine's Linktree](https://linktr.ee/the.real.charmainee)"
    )

    st.write("Thank you for supporting biomedical data exploration.")
