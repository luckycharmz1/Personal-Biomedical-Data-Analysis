
# =========================
# IMPORTS
# =========================
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu


# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Biomedical Dashboard",
    page_icon="🧬",
    layout="wide"
)


# =========================
# FILE PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent

# Main folder containing your Samsung Health export.
# CSV files may be nested inside additional folders.
data_folder = BASE_DIR / "Samsung Health"

pictures_folder = BASE_DIR / "pictures"


# =========================
# HELPER FUNCTIONS
# =========================
def get_csv_files(folder):
    """Find CSV files in the folder and all its subfolders."""
    if not folder.exists() or not folder.is_dir():
        return []

    return sorted(
        file for file in folder.rglob("*.csv")
        if file.is_file()
    )


def read_csv_file(file_path):
    """Read a CSV file and handle common encoding differences."""
    return pd.read_csv(
        file_path,
        encoding="utf-8-sig",
        on_bad_lines="warn"
    )


def get_numeric_columns(df):
    """Identify columns that contain usable numeric measurements."""
    numeric_data = {}

    for col in df.columns:
        column_name = str(col).lower()

        # Avoid treating identifiers and date/time fields as measurements.
        if any(word in column_name for word in [
            "date", "time", "timestamp", "id"
        ]):
            continue

        # First try to interpret the column as numeric.
        values = pd.to_numeric(df[col], errors="coerce")

        # Include the column only if at least one value is numeric.
        if values.notna().any():
            numeric_data[str(col)] = values

    return pd.DataFrame(numeric_data)


# =========================
# DATA ANALYSIS NOTICE
# =========================
def show_data_analysis_notice():
    with st.expander("🧬 Data analysis notice"):
        st.info(
            """
            **Current project limitation**

            Samsung Health exports can contain complex CSV structures,
            including timestamps, metadata, text fields, and measurements
            that may require additional processing before they can be
            graphed correctly.

            I am continuing to develop my data analysis skills and
            exploring MATLAB and Python to improve how these files
            are processed and visualized.

            If a graph cannot be generated or numeric measurements
            are not detected, the data may need additional cleaning
            or format-specific processing.

            Missing graphs do not necessarily mean that the underlying
            health measurements are absent.
            """
        )


# =========================
# SIDEBAR NAVIGATION
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
# HOME PAGE
# =========================
if selected == "Home":
    st.title("🧬 Charmaine's Biomedical Data Dashboard")

    st.markdown(
        """
        Welcome to my biomedical data exploration dashboard.

        This project bridges science and technology, combining my
        interest in data with my lived experience with sickle cell anemia.

        From September 2025 to December 2025, I participated in the
        Stanford University Science Small Group, where I learned about
        research and hypothesis development.

        I have continued exploring wearable technology and sickle cell
        disease through my own independent research. I appreciate my
        mentor, Dr. Nowah Afangbedii, for helping me develop my research
        skills.

        This dashboard explores historical wearable data to investigate
        trends and potential patterns over time.

        **Important:** This project is exploratory and is not intended
        for medical diagnosis or predicting sickle cell crises.
        """
    )

    st.divider()

    st.info("This is an evolving research and portfolio project.")

    st.markdown(
        """
        ### Unofficial Scientific Research Paper

        This paper currently contains preliminary observations and
        hypotheses. It is not a completed experiment.

        [Read Charmaine's Unofficial Scientific Research Paper](https://docs.google.com/document/d/1v469ivc47A7XoQT55V1xtfQh5k40MWHi3-0tb7b99n0/edit?usp=sharing)
        """
    )


# =========================
# DATA VIEWER PAGE
# =========================
elif selected == "Data Viewer":
    st.header("Samsung Health Data Viewer")

    # Notice appears only on the Data Viewer page.
    show_data_analysis_notice()

    st.write(
        "Browse your Samsung Health CSV files and inspect the "
        "underlying data before creating visualizations."
    )

    if not data_folder.exists():
        st.error(f"Samsung Health folder not found: {data_folder}")

    else:
        all_files = get_csv_files(data_folder)

        if not all_files:
            st.warning(
                "No CSV files were found. Check that your CSV files "
                "are uploaded inside the Samsung Health folder."
            )

        else:
            st.success(f"Found {len(all_files)} CSV file(s).")

            selected_file = st.selectbox(
                "Choose a CSV file to inspect",
                all_files,
                format_func=lambda file: str(
                    file.relative_to(data_folder)
                ),
                key="viewer_file"
            )

            try:
                df = read_csv_file(selected_file)

                st.write("File:", selected_file.name)
                st.write(
                    "File size (bytes):",
                    selected_file.stat().st_size
                )
                st.write("Rows loaded:", df.shape[0])
                st.write("Columns loaded:", df.shape[1])
                st.write("Column names:", df.columns.tolist())

                st.subheader("Raw CSV preview")

                raw_df = pd.read_csv(
                    selected_file,
                    header=None,
                    sep=None,
                    engine="python",
                    encoding="utf-8-sig",
                    skip_blank_lines=True,
                    nrows=8,
                    on_bad_lines="warn"
                )

                st.dataframe(
                    raw_df,
                    use_container_width=True
                )

                if df.empty:
                    st.warning("This CSV file contains no data.")

                else:
                    st.subheader(selected_file.name)

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Rows", df.shape[0])
                    col2.metric("Columns", df.shape[1])
                    col3.metric(
                        "Missing values",
                        int(df.isna().sum().sum())
                    )

                    st.markdown("### Data Preview")

                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=450
                    )

                    with st.expander("Column information"):
                        column_info = pd.DataFrame({
                            "Column": df.columns.astype(str),
                            "Data type": [
                                str(dtype) for dtype in df.dtypes
                            ],
                            "Missing values": [
                                int(value)
                                for value in df.isna().sum()
                            ]
                        })

                        st.dataframe(
                            column_info,
                            use_container_width=True
                        )

            except Exception as e:
                st.error(
                    f"Could not read {selected_file.name}: {e}"
                )


# =========================
# GRAPHS PAGE
# =========================
elif selected == "Graphs":
    st.header("Interactive Biomedical Graphs")

    # Notice appears only on the Graphs page.
    show_data_analysis_notice()

    st.write(
        "Select a dataset and numeric measurement to explore "
        "potential trends in your wearable data."
    )

    if not data_folder.exists():
        st.error(f"Samsung Health folder not found: {data_folder}")

    else:
        all_files = get_csv_files(data_folder)

        if not all_files:
            st.warning(
                "No CSV files were found in the Samsung Health folder."
            )

        else:
            selected_file = st.selectbox(
                "Select a dataset",
                all_files,
                format_func=lambda file: str(
                    file.relative_to(data_folder)
                ),
                key="graph_file"
            )

            try:
                df = read_csv_file(selected_file)

                if df.empty:
                    st.warning("This CSV file contains no data.")

                else:
                    st.subheader(selected_file.name)

                    numeric_df = get_numeric_columns(df)

                    if numeric_df.empty:
                        st.warning(
                            "No numeric measurement columns were found "
                            "in this file. Check the Data Viewer to "
                            "inspect its column names and contents."
                        )

                    else:
                        metric = st.selectbox(
                            "Select a numeric measurement",
                            list(numeric_df.columns),
                            key="graph_metric"
                        )

                        # Look for a date/time column to use on the
                        # horizontal axis when one is available.
                        date_column = next(
                            (
                                col for col in df.columns
                                if any(
                                    word in str(col).lower()
                                    for word in [
                                        "date", "time", "timestamp"
                                    ]
                                )
                            ),
                            None
                        )

                        plot_df = pd.DataFrame({
                            "Measurement": numeric_df[metric]
                        })

                        if date_column is not None:
                            parsed_dates = pd.to_datetime(
                                df[date_column],
                                errors="coerce"
                            )

                            if parsed_dates.notna().sum() > 0:
                                plot_df["Date/Time"] = parsed_dates

                                plot_df = plot_df.dropna(
                                    subset=[
                                        "Date/Time",
                                        "Measurement"
                                    ]
                                )

                                plot_df = plot_df.sort_values(
                                    "Date/Time"
                                )

                                fig = px.line(
                                    plot_df,
                                    x="Date/Time",
                                    y="Measurement",
                                    title=f"{metric} over time",
                                    markers=True
                                )

                            else:
                                plot_df = plot_df.dropna(
                                    subset=["Measurement"]
                                )

                                fig = px.line(
                                    plot_df,
                                    y="Measurement",
                                    title=metric,
                                    markers=True
                                )

                        else:
                            plot_df = plot_df.dropna(
                                subset=["Measurement"]
                            )

                            fig = px.line(
                                plot_df,
                                y="Measurement",
                                title=metric,
                                markers=True
                            )

                        if plot_df.empty:
                            st.warning(
                                "There are no usable values to plot "
                                "for this measurement."
                            )

                        else:
                            fig.update_traces(
                                line=dict(color="purple")
                            )

                            fig.update_layout(
                                xaxis_title="Date/Time or Row Number",
                                yaxis_title=metric
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                            st.caption(
                                "Explore these charts as descriptive "
                                "visualizations. They do not establish "
                                "causation or predict medical events."
                            )

            except Exception as e:
                st.error(
                    f"Error processing {selected_file.name}: {e}"
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

    # Research experience
    st.subheader("Research Experience")

    st.markdown("### Stanford University Science Small Group")
    st.caption("September–December 2025")

    st.write(
        "Participated in a four-month research program focused on "
        "research skills and hypothesis development, exploring "
        "potential physiological patterns related to sickle cell disease."
    )

    stanford_certificate = (
        pictures_folder / "ssg.png"
    )

    if stanford_certificate.exists():
        st.image(
            str(stanford_certificate),
            caption=(
                "Stanford University Science Small Group — "
                "Certificate of Completion"
            ),
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

    # Training and coursework
    st.subheader("Relevant Coursework & Training")

    st.markdown("### Python for Health Sciences and Healthcare")
    st.caption("Completed — October 2026")

    st.write(
        "Completed training in Python applications relevant to "
        "health sciences and healthcare data analysis."
    )

    python_certificate = (
        pictures_folder / "linkedin_certificate.jpeg"
    )

    if python_certificate.exists():
        st.image(
            str(python_certificate),
            caption=(
                "Python for Health Sciences and Healthcare — Certificate"
            ),
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

    # Independent project
    st.subheader("Independent Project")

    st.markdown("### Personal Biomedical Data Analysis Dashboard")

    st.write(
        "Developing a Python and Streamlit application to explore "
        "historical Samsung Health data and investigate potential "
        "relationships between wearable measurements, lifestyle "
        "factors, and recorded symptoms."
    )

    st.info(
        "This is an exploratory research project. It is not intended "
        "to diagnose medical conditions or predict sickle cell crises."
    )


# =========================
# CONTACT PAGE
# =========================
elif selected == "Contact":
    st.header("Contact")

    st.markdown(
        "🌐 Connect with me here: "
        "[Charmaine's Linktree](https://linktr.ee/the.real.charmainee)"
    )

    st.write(
        "Thank you for supporting biomedical data exploration."
    )
