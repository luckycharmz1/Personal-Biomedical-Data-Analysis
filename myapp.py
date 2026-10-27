
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
    page_icon="🧬",
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
            "Research Background",
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
# This should be the folder containing your CSV files.
data_folder = Path("Samsung Health")


# =========================
# HOME PAGE
# =========================
if selected == "Home":
    st.title("Charmaine's Biomedical Data Dashboard")

    st.markdown(
        """
        Welcome to my biomedical data exploration dashboard.

        This project bridges science and technology, combining
        my interest in data with my lived experience with
        sickle cell disease.

        I am conducting independent exploratory work using
        historical health data to investigate potential
        relationships between biometric measurements,
        lifestyle factors, and recorded symptoms.

        I am also exploring wearable technology as a future
        part of this project.

        This dashboard is a work in progress. Its purpose is
        to organize and explore data over time.

        ⚠️ This tool is exploratory and is not intended
        for medical diagnosis or treatment decisions.
        """
    )

    st.markdown("---")
    st.info("This is an evolving research and portfolio project.")

    st.markdown(
        """
        ### Research Paper

        I am documenting the development of this project in
        a working research paper. The paper currently includes
        my observations and research hypothesis and is still
        under development.

        [Read Charmaine's Working Research Paper](https://docs.google.com/document/d/1v469ivc47A7XoQT55V1xtfQh5k40MWHi3-0tb7b99n0/edit?usp=sharing)
        """
    )


# =========================
# DATA VIEWER PAGE
# =========================
elif selected == "Data Viewer":
    st.header("Samsung Health Data Viewer")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(
            f"Folder '{data_folder}' does not exist. "
            "Check that your Samsung Health folder is included "
            "in your project repository."
        )
    else:
        all_files = sorted(
            f for f in data_folder.glob("*.csv") if f.is_file()
        )

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset to view",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                df = pd.read_csv(
                    selected_file,
                    header=None,
                    engine="python",
                    on_bad_lines="skip"
                )

                # Clean quotation marks and whitespace.
                df = df.map(
                    lambda x: (
                        x.replace('"', '').strip()
                        if isinstance(x, str)
                        else x
                    )
                )

                st.subheader("Preview")
                st.dataframe(df.head(), use_container_width=True)

                st.subheader("Basic Information")
                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")

            except pd.errors.EmptyDataError:
                st.warning(
                    f"{selected_file.name} is empty "
                    "and could not be loaded."
                )
            except Exception as e:
                st.error(f"Error reading file: {e}")


# =========================
# GRAPHS PAGE
# =========================
elif selected == "Graphs":
    st.header("Interactive Biomedical Graphs")

    if not data_folder.exists() or not data_folder.is_dir():
        st.error(f"Folder '{data_folder}' does not exist.")
    else:
        all_files = sorted(
            f for f in data_folder.glob("*.csv") if f.is_file()
        )

        if not all_files:
            st.warning("No CSV files found in the folder.")
        else:
            selected_file = st.selectbox(
                "Select dataset to visualize",
                all_files,
                format_func=lambda x: x.name
            )

            try:
                df = pd.read_csv(
                    selected_file,
                    header=None,
                    engine="python",
                    on_bad_lines="skip"
                )

                if df.empty:
                    st.warning("CSV file is empty.")

                else:
                    # Single-column CSV
                    if df.shape[1] == 1:
                        col_name = selected_file.stem
                        df_numeric = pd.to_numeric(
                            df.iloc[:, 0],
                            errors="coerce"
                        ).dropna()

                        if df_numeric.empty:
                            st.warning(
                                "No numeric values were found "
                                "in this dataset."
                            )
                        else:
                            st.subheader(col_name)

                            fig = px.line(
                                x=df_numeric.index,
                                y=df_numeric.values,
                                labels={
                                    "x": "Record Index",
                                    "y": col_name
                                },
                                title=col_name
                            )

                            fig.update_traces(
                                line=dict(color="purple")
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                    # Multi-column CSV
                    else:
                        df_numeric = pd.DataFrame()

                        for i, col in enumerate(df.columns):
                            col_name = (
                                f"{selected_file.stem}_col{i + 1}"
                            )

                            temp_col = (
                                df[col]
                                .astype(str)
                                .str.replace(
                                    r"[^0-9.-]",
                                    "",
                                    regex=True
                                )
                            )

                            df_numeric[col_name] = pd.to_numeric(
                                temp_col,
                                errors="coerce"
                            )

                        # Only display columns containing numbers.
                        valid_columns = [
                            col for col in df_numeric.columns
                            if df_numeric[col].notna().any()
                        ]

                        if not valid_columns:
                            st.warning(
                                "No numeric data could be extracted "
                                "from this CSV file."
                            )
                        else:
                            metric = st.selectbox(
                                "Select metric to analyze",
                                valid_columns
                            )

                            plot_data = df_numeric[metric].dropna()

                            st.subheader(metric)

                            fig = px.line(
                                x=plot_data.index,
                                y=plot_data.values,
                                labels={
                                    "x": "Record Index",
                                    "y": metric
                                },
                                title=metric
                            )

                            fig.update_traces(
                                line=dict(color="purple")
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

            except Exception as e:
                st.error(
                    f"Error processing {selected_file.name}: {e}"
                )


# =========================
# RESEARCH BACKGROUND PAGE
# =========================
elif selected == "Research Background":
    st.title("Research Background & Learning")

    st.markdown(
        """
        This section highlights the research experiences,
        scientific training, and technical learning that
        contribute to my independent biomedical data analysis
        project.
        """
    )

    st.divider()

    # -------------------------
    # Research Experience
    # -------------------------
    st.header("🔬 Research Experience")

    with st.container(border=True):
        st.subheader("Stanford University")

        st.caption("Research Internship | May–August 2024")

        st.write(
            "During my internship, my work primarily involved "
            "Lyme disease and E. coli. This experience is part "
            "of my broader background in biological and "
            "biomedical research."
        )

        st.caption(
            "Additional details about my specific responsibilities "
            "and research techniques can be added here."
        )

    # -------------------------
    # Scientific Training
    # -------------------------
    st.header("🧪 Scientific Training")

    with st.container(border=True):
        st.subheader("Science Small Group")

        st.caption("September–December 2025")

        st.write(
            "I participated in a Science Small Group where "
            "I learned foundational research skills, including "
            "developing hypotheses and formulating scientific "
            "research questions."
        )

        st.write(
            "This training helped me develop the foundation "
            "for investigating potential physiological patterns "
            "associated with sickle cell disease."
        )

        st.caption(
            "Mentor: Dr. Nowah Afangbedii"
        )

    # -------------------------
    # Certifications & Courses
    # -------------------------
    st.header("🎓 Certifications & Coursework")

    with st.container(border=True):
        st.subheader(
            "Python for Health Sciences and Healthcare"
        )

        st.caption("Completed | October 2026")

        st.write(
            "Completed coursework focused on Python and "
            "its applications in health sciences and healthcare."
        )

    with st.container(border=True):
        st.subheader(
            "Biology Meets Programming: Bioinformatics for Beginners"
        )

        st.caption("In progress")

        st.write(
            "Studying introductory programming concepts "
            "and their applications in biological data "
            "and bioinformatics."
        )

    st.caption(
        "Additional certifications can be listed here as "
        "they are completed. Include links to certificates "
        "when available."
    )

    # -------------------------
    # Connection to the Project
    # -------------------------
    st.divider()

    st.header("💡 How This Supports My Project")

    st.write(
        "My experiences in biological research and scientific "
        "training inform my interest in biomedical data analysis. "
        "I am building on this background by using Python to "
        "explore historical health data and by studying robotics "
        "and embedded systems for future wearable technology "
        "development."
    )

    st.info(
        "This page describes my research background and learning. "
        "The experiences listed here do not independently validate "
        "the medical significance of patterns explored in this app."
    )


# =========================
# CONTACT PAGE
# =========================
elif selected == "Contact":
    st.header("Contact")

    st.markdown(
        """
        🌐 Connect with me here:

        [Charmaine's Linktree](https://linktr.ee/the.real.charmainee)
        """
    )

    st.write(
        "Thank you for supporting biomedical data exploration."
    )
