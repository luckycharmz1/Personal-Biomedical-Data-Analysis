
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Charmaine's Biomedical Data Dashboard",
    page_icon="🧬",
    layout="wide"
)


# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
data_folder = BASE_DIR / "Samsung Health"
pictures_folder = BASE_DIR / "pictures"


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_csv_files(folder):
    """Find CSV files in a folder and all its subfolders."""
    if not folder.exists() or not folder.is_dir():
        return []

    return sorted(
        file for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() == ".csv"
    )


def read_csv_file(file_path):
    """Try common CSV delimiters and return the best parsed table."""
    best_df = None
    best_score = -1

    for separator in [",", ";", "\t", "|"]:
        try:
            df = pd.read_csv(
                file_path,
                sep=separator,
                encoding="utf-8-sig",
                on_bad_lines="warn",
                skip_blank_lines=True,
                low_memory=False
            )

            # Prefer files that parse into multiple columns.
            if df.shape[1] > 1:
                score = df.shape[1] * 1000 + df.shape[0]

                if score > best_score:
                    best_df = df
                    best_score = score

        except Exception:
            continue

    if best_df is not None:
        return best_df

    # Fallback for files using an unusual delimiter.
    return pd.read_csv(
        file_path,
        sep=None,
        engine="python",
        encoding="utf-8-sig",
        on_bad_lines="warn",
        skip_blank_lines=True,
        low_memory=False
    )


def get_numeric_columns(df):
    """Identify columns that contain mostly numeric values."""
    numeric_data = {}

    excluded_words = [
        "date", "time", "timestamp", "uuid", "guid",
        "device_id", "user_id"
    ]

    for col in df.columns:
        name = str(col).strip().lower()

        if any(word in name for word in excluded_words):
            continue

        original = df[col]

        cleaned = (
            original.astype("string")
            .str.strip()
            .str.replace(",", "", regex=False)
        )

        values = pd.to_numeric(cleaned, errors="coerce")
        nonempty_count = original.notna().sum()

        if nonempty_count == 0:
            continue

        numeric_ratio = values.notna().sum() / nonempty_count

        if numeric_ratio >= 0.80 and values.notna().sum() >= 2:
            numeric_data[str(col)] = values

    return pd.DataFrame(numeric_data, index=df.index)


def show_data_analysis_notice():
    """Explain current limitations of the data-processing features."""
    with st.expander("💡 Data analysis tip and current limitations"):
        st.info(
            """
            **Current project limitation**

            Samsung Health exports can contain complex CSV structures,
            including timestamps, metadata, text fields, and measurements
            that may require additional processing before they can be graphed.

            This dashboard is still being developed to interpret these
            files correctly. If no numeric measurements are detected,
            the data may need additional cleaning or format-specific
            processing.

            **Next steps:** I am continuing to develop my data analysis
            skills and exploring tools such as MATLAB and Python to
            improve data processing and visualization.

            Please do not interpret missing graphs as evidence that
            the underlying health measurements are absent.
            """
        )


def show_image_if_available(image_name, caption=None):
    """Display a project image only when the file exists."""
    image_path = pictures_folder / image_name

    if image_path.is_file():
        st.image(str(image_path), caption=caption, width=350)


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:
    st.title("🧬 Biomedical Data")

    selected = option_menu(
        menu_title="Navigation",
        options=[
            "Home",
            "Data Viewer",
            "Graphs",
            "Research Background & Credentials",
            "Contact"
        ],
        icons=[
            "house",
            "table",
            "bar-chart",
            "mortarboard",
            "envelope"
        ],
        menu_icon="activity",
        default_index=0
    )

    st.divider()

    st.caption(
        "An independent project exploring biomedical data, "
        "wearable technology, and health research."
    )


# ==================================================
# HOME PAGE
# ==================================================

if selected == "Home":

    st.title("Charmaine's Biomedical Data Dashboard")

    st.subheader(
        "Exploring the intersection of science, data, "
        "wearable technology, and lived experience"
    )

    st.write(
        """
        Welcome to my biomedical data dashboard!

        This independent project brings together my interests in
        biological sciences, programming, and healthcare analytics.
        I am exploring how wearable technology and personal health
        data can help me investigate patterns in everyday measurements
        and my lived experience with sickle cell anemia.
        """
    )

    st.info(
        "This dashboard is an educational and exploratory project. "
        "It is not intended to diagnose, treat, or predict medical "
        "conditions or sickle cell crises."
    )

    st.markdown("### Project Background")

    st.write(
        """
        From September to December 2025, I participated in the
        Stanford University Science Small Group, where I explored
        scientific questions and hypothesis development.

        Building on that experience, I am independently exploring
        wearable health data and sickle cell anemia. My goal is to
        develop my skills in Python, data processing, visualization,
        and biomedical research.
        """
    )

    st.markdown("### Research Paper")

    st.write(
        "Read more about my research and project background:"
    )

    st.markdown(
        "[View my research paper on Google Docs]"
        "(https://docs.google.com/document/d/"
        "1v469ivc47A7XoQT55V1xtfQh5k40MWHi-3"
        "0tb7b99n0/edit?usp=sharing)"
    )

    st.markdown("### Explore the Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Data Viewer**")
        st.write(
            "Inspect CSV files, column names, missing values, "
            "and imported data."
        )

    with col2:
        st.markdown("**Interactive Graphs**")
        st.write(
            "Explore numeric measurements visually when the "
            "selected data can be processed successfully."
        )


# ==================================================
# DATA VIEWER PAGE
# ==================================================

elif selected == "Data Viewer":

    st.header("Samsung Health Data Viewer")

    show_data_analysis_notice()

    st.write(
        "Browse your Samsung Health CSV files and inspect the "
        "underlying data before creating visualizations."
    )

    if not data_folder.exists():
        st.error(
            f"Samsung Health folder not found: {data_folder}"
        )

        st.warning(
            "Check that the Samsung Health folder is in the same "
            "project directory as myapp.py."
        )

    else:
        all_files = get_csv_files(data_folder)

        if not all_files:
            st.warning(
                "No CSV files were found. Check that your CSV files "
                "are stored inside the Samsung Health folder."
            )

        else:
            st.success(
                f"Found {len(all_files)} CSV file(s)."
            )

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

                st.subheader(selected_file.name)

                col1, col2, col3 = st.columns(3)

                col1.metric("Rows", df.shape[0])
                col2.metric("Columns", df.shape[1])
                col3.metric(
                    "Missing values",
                    int(df.isna().sum().sum())
                )

                st.markdown("### Imported Data")

                st.dataframe(
                    df,
                    use_container_width=True,
                    height=450
                )

                with st.expander("Inspect raw CSV preview"):

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

                    st.write(
                        "These are the first rows as interpreted "
                        "without using the first row as column names."
                    )

                    st.dataframe(
                        raw_df,
                        use_container_width=True
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


# ==================================================
# GRAPHS PAGE
# ==================================================

elif selected == "Graphs":

    st.header("Interactive Biomedical Graphs")

    show_data_analysis_notice()

    st.write(
        """
        Select a Samsung Health CSV file and explore its numeric
        columns. These visualizations are intended for exploratory
        analysis, not medical interpretation.
        """
    )

    if not data_folder.exists():
        st.warning(
            "The Samsung Health folder was not found. "
            "Add the folder to your project directory."
        )

    else:
        all_files = get_csv_files(data_folder)

        if not all_files:
            st.warning(
                "No CSV files were found inside the Samsung Health folder."
            )

        else:
            selected_graph_file = st.selectbox(
                "Choose a CSV file to graph",
                all_files,
                format_func=lambda file: str(
                    file.relative_to(data_folder)
                ),
                key="graph_file"
            )

            try:
                graph_df = read_csv_file(selected_graph_file)
                numeric_df = get_numeric_columns(graph_df)

                if numeric_df.empty:
                    st.warning(
                        "No numeric measurement columns were detected "
                        "in this file. The file may contain metadata, "
                        "non-numeric measurements, unusual headers, "
                        "or a format that needs additional cleaning."
                    )

                    st.markdown(
                        "**Try this:** Open the Data Viewer page and "
                        "inspect the imported data and raw CSV preview. "
                        "Those views can help identify how the file "
                        "needs to be processed."
                    )

                else:
                    st.success(
                        f"Detected {len(numeric_df.columns)} "
                        "potential numeric column(s)."
                    )

                    selected_columns = st.multiselect(
                        "Choose measurement(s) to graph",
                        options=list(numeric_df.columns),
                        default=list(numeric_df.columns[:1])
                    )

                    if selected_columns:

                        chart_df = numeric_df[selected_columns].copy()
                        chart_df = chart_df.dropna(how="all")

                        chart_type = st.selectbox(
                            "Choose a chart type",
                            [
                                "Line chart",
                                "Scatter plot",
                                "Histogram",
                                "Box plot"
                            ]
                        )

                        if chart_type == "Line chart":
                            fig = px.line(
                                chart_df,
                                y=selected_columns,
                                title="Selected Measurements"
                            )

                            fig.update_xaxes(
                                title="Row number"
                            )

                            fig.update_yaxes(
                                title="Measurement value"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                        elif chart_type == "Scatter plot":

                            if len(selected_columns) < 2:
                                st.info(
                                    "Select at least two numeric "
                                    "columns to create a scatter plot."
                                )

                            else:
                                x_column = st.selectbox(
                                    "Select the X-axis",
                                    selected_columns,
                                    key="scatter_x"
                                )

                                y_options = [
                                    column
                                    for column in selected_columns
                                    if column != x_column
                                ]

                                y_column = st.selectbox(
                                    "Select the Y-axis",
                                    y_options,
                                    key="scatter_y"
                                )

                                fig = px.scatter(
                                    chart_df,
                                    x=x_column,
                                    y=y_column,
                                    title=f"{y_column} vs. {x_column}"
                                )

                                st.plotly_chart(
                                    fig,
                                    use_container_width=True
                                )

                        elif chart_type == "Histogram":

                            histogram_column = st.selectbox(
                                "Select a measurement",
                                selected_columns,
                                key="histogram_column"
                            )

                            fig = px.histogram(
                                chart_df,
                                x=histogram_column,
                                title=f"Distribution of {histogram_column}"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                        elif chart_type == "Box plot":

                            fig = px.box(
                                chart_df,
                                y=selected_columns,
                                title="Measurement Distributions"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                        with st.expander("View data used for the graph"):
                            st.dataframe(
                                chart_df,
                                use_container_width=True
                            )

                    else:
                        st.info(
                            "Select at least one measurement to create a graph."
                        )

            except Exception as e:
                st.error(
                    f"Could not create a graph from "
                    f"{selected_graph_file.name}: {e}"
                )


# ==================================================
# RESEARCH BACKGROUND & CREDENTIALS PAGE
# ==================================================

elif selected == "Research Background & Credentials":

    st.header("Research Background & Credentials")

    st.write(
        """
        My academic interests center on the intersection of biological
        sciences, biomedical research, programming, and healthcare data.
        This page highlights experiences that have contributed to my
        ongoing learning.
        """
    )

    st.markdown("### Stanford University Science Small Group")

    st.write(
        """
        **September–December 2025**

        Participated in a science learning group focused on scientific
        exploration, developing research questions, and hypothesis
        development.
        """
    )

    show_image_if_available(
        "ssg.png",
        caption="Stanford University Science Small Group certificate"
    )

    st.divider()

    st.markdown("### Stanford University Internship")

    st.write(
        """
        **May–August 2024**

        Gained exposure to research involving Lyme disease and
        *Escherichia coli* (E. coli), strengthening my interest in
        biological research and scientific investigation.
        """
    )

    st.divider()

    st.markdown(
        "### Python for Health Sciences and Healthcare"
    )

    st.write(
        """
        **Completed October 2026**

        Completed training in Python applications relevant to
        health sciences and healthcare analytics.
        """
    )

    show_image_if_available(
        "linkedin_certificate.jpeg",
        caption="Python for Health Sciences and Healthcare certificate"
    )

    st.divider()

    st.markdown(
        "### Biology Meets Programming: Bioinformatics for Beginners"
    )

    st.write(
        """
        **UC San Diego — In progress**

        Exploring programming concepts and their applications
        in biological data and bioinformatics.
        """
    )

    st.divider()

    st.markdown("### Independent Biomedical Data Project")

    st.write(
        """
        This dashboard is an ongoing learning project exploring
        Samsung Health exports, data cleaning, and visualization.

        I am continuing to develop my Python skills and investigate
        how wearable measurements can be organized for exploratory
        biomedical research.

        The project is not a validated clinical tool and does not
        diagnose conditions or predict sickle cell crises.
        """
    )


# ==================================================
# CONTACT PAGE
# ==================================================

elif selected == "Contact":

    st.header("Contact")

    st.write(
        """
        Thank you for visiting my biomedical data dashboard.
        I am interested in science, biomedical research, programming,
        and opportunities at the intersection of technology and health.
        """
    )

    st.markdown(
        "[Connect with me through my Linktree]"
        "(https://linktr.ee/the.real.charmainee)"
    )

    st.caption(
        "This dashboard is an independent educational project."
    )
