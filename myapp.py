
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
        "Participated in research learning and hypothesis development, "
        "exploring potential physiological patterns related to "
        "sickle cell disease."
    )

    stanford_certificate = (
        Path("pictures") /
        "Certificate_Completion_Charmain Washington.jpeg"
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
