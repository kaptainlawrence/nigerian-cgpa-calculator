
import streamlit as st

# Configure the browser page.
st.set_page_config(
    page_title="Nigerian University CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# Create the grading functions.
def get_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    else:
        return "F"


def get_grade_point(score):
    if score >= 70:
        return 5.0
    elif score >= 60:
        return 4.0
    elif score >= 50:
        return 3.0
    elif score >= 45:
        return 2.0
    elif score >= 40:
        return 1.0
    else:
        return 0.0


def get_classification(cgpa):
    if cgpa >= 4.50:
        return "First Class Honours"
    elif cgpa >= 3.50:
        return "Second Class Honours (Upper Division)"
    elif cgpa >= 2.40:
        return "Second Class Honours (Lower Division)"
    elif cgpa >= 1.50:
        return "Third Class Honours"
    elif cgpa >= 1.00:
        return "Pass"
    else:
        return "Below the listed classification thresholds"


# Set the website heading.
st.title("🎓 Nigerian University CGPA Calculator")
st.caption(
    "Calculate your GPA using the Nigerian 5.0 grading scale."
)

# Show the grading guide in an expandable section.
with st.expander("View grading scale and classifications"):
    st.markdown("""
    | Score | Grade | Grade Point |
    |---|---|---:|
    | 70–100% | A | 5.0 |
    | 60–69% | B | 4.0 |
    | 50–59% | C | 3.0 |
    | 45–49% | D | 2.0 |
    | 40–44% | E | 1.0 |
    | 0–39% | F | 0.0 |
    """)

    st.caption(
        "Classification: First Class 4.50–5.00; "
        "Second Class Upper 3.50–4.49; "
        "Second Class Lower 2.40–3.49; "
        "Third Class 1.50–2.39; Pass 1.00–1.49."
    )

# Keep the courses in memory during the session.
if "courses" not in st.session_state:
    st.session_state.courses = []

# Create the course entry form.
st.subheader("Add a course")

with st.form("course_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Course name", placeholder="CSC101")

    with col2:
        score = st.number_input(
            "Score (%)", min_value=0.0,
            max_value=100.0, value=75.0, step=1.0
        )

    with col3:
        units = st.number_input(
            "Credit units", min_value=1,
            max_value=30, value=3, step=1
        )

    submitted = st.form_submit_button(
        "➕ Add Course", use_container_width=True
    )

# Add the course only when the form is submitted.
if submitted:
    if not name.strip():
        st.error("Please enter a course name.")
    elif any(
        c["Course"].casefold() == name.strip().casefold()
        for c in st.session_state.courses
    ):
        st.error("That course name has already been entered.")
    else:
        point = get_grade_point(score)

        st.session_state.courses.append({
            "Course": name.strip(),
            "Score": score,
            "Grade": get_grade(score),
            "Grade Point": point,
            "Credit Units": int(units),
            "Quality Points": point * int(units)
        })

        st.rerun()

# Display the courses and calculate the result.
if st.session_state.courses:
    st.subheader("Courses entered")

    st.dataframe(
        st.session_state.courses,
        use_container_width=True,
        hide_index=True
    )

    total_units = sum(
        c["Credit Units"] for c in st.session_state.courses
    )

    total_quality = sum(
        c["Quality Points"] for c in st.session_state.courses
    )

    # Calculate GPA from quality points and credit units.
    cgpa = total_quality / total_units

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Credit Units", total_units)
    col2.metric("Total Quality Points", f"{total_quality:.1f}")
    col3.metric("GPA / CGPA", f"{cgpa:.2f}")

    st.success(
        "Estimated Classification: "
        + get_classification(cgpa)
    )

    # Let the user remove the most recently entered course.
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Undo Last Course", use_container_width=True):
            st.session_state.courses.pop()
            st.rerun()

    with col2:
        if st.button("Clear All Courses", use_container_width=True):
            st.session_state.courses = []
            st.rerun()

else:
    st.info("Enter your first course above to get started.")

# Explain the limitation of the calculation.
st.divider()
st.caption(
    "Educational tool. Results use the supplied grading scale. "
    "Confirm your university's official grading and classification rules."
)
