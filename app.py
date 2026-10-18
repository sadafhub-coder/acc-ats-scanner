# app.py
import streamlit as st
import pandas as pd
from skills_data import ROLE_SKILLS, RECOMMENDED_MODULES
from parser import extract_text_from_pdf, extract_text_from_docx, analyze_resume

# Page Setup
st.set_page_config(
    page_title="ACC ATS Resume & Skill-Gap Scanner",
    page_icon="📊",
    layout="wide"
)

# Custom Accent Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .badge-found {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        background-color: #1e4620;
        color: #7ced85;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-missing {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        background-color: #4d1d1d;
        color: #ff9b9b;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .mentor-card {
        background: linear-gradient(135deg, #0e1e38 0%, #172a45 100%);
        border: 1px solid #1f3b64;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown('<div class="main-title">📈 Analytics Career Connect (ACC)</div>', unsafe_allow_html=True)
    st.caption("AI-Powered Resume ATS Optimization & Technical Competency Evaluator")

st.markdown("---")

# Input Section
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("1. Target Role & Objective")
    selected_role = st.selectbox("Select Target Analytics Role:", list(ROLE_SKILLS.keys()))
    role_data = ROLE_SKILLS[selected_role]
    st.info(f"Scanning against **{selected_role}** core requirements (Databases, Analytics, BI, and Tools).")

with col_right:
    st.subheader("2. Upload Resume")
    uploaded_file = st.file_uploader("Upload Resume (.pdf or .docx):", type=["pdf", "docx"])
    pasted_text = st.text_area("Or paste your resume text here:", height=105, placeholder="Paste text here if you don't have a file ready...")

run_scan = st.button("🚀 Analyze Resume & Reveal ATS Score", type="primary", use_container_width=True)

# Results Processing
if run_scan:
    resume_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)
    elif pasted_text.strip():
        resume_text = pasted_text.strip()
    else:
        st.error("Please provide a resume by uploading a file or pasting text.")

    if resume_text:
        score, results = analyze_resume(resume_text, role_data)
        st.session_state["score"] = score
        st.session_state["results"] = results
        st.session_state["scanned_role"] = selected_role

if "score" in st.session_state:
    score = st.session_state["score"]
    results = st.session_state["results"]
    selected_role = st.session_state["scanned_role"]

    st.markdown("---")
    st.subheader("📊 Executive Analysis & Performance Score")

    # Top Metric Display
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="Overall ATS Match Score", 
            value=f"{score}%", 
            delta=f"{score - 75}% vs 75% Target" if score >= 75 else f"{score - 75}% Short of 75%"
        )
    with m2:
        status = "Strong Profile" if score >= 75 else ("Interview Contender" if score >= 50 else "High Risk - Gaps Found")
        st.metric(label="ATS Screening Tier", value=status)
    with m3:
        total_missing = sum(len(d["missing"]) for d in results.values())
        st.metric(label="Identified Missing Skills", value=f"{total_missing} Skills")

    st.progress(score / 100)

    # Visual Chart: Category Match Breakdown
    cat_names = []
    cat_pcts = []
    for category, data in results.items():
        total = len(data["found"]) + len(data["missing"])
        pct = round((len(data["found"]) / total) * 100) if total > 0 else 0
        cat_names.append(category)
        cat_pcts.append(pct)

    df_chart = pd.DataFrame({"Category": cat_names, "Competency Match (%)": cat_pcts}).set_index("Category")
    
    col_chart, col_recom = st.columns([1.2, 1], gap="medium")
    
    with col_chart:
        st.markdown("#### 🎯 Domain Coverage")
        st.bar_chart(df_chart, horizontal=True)

    with col_recom:
        st.markdown("#### 🚀 ACC Recommended Sprints")
        recommended_courses = []
        for category, data in results.items():
            if data["missing"] and category in RECOMMENDED_MODULES:
                recommended_courses.append(RECOMMENDED_MODULES[category])

        if recommended_courses:
            for c in list(set(recommended_courses)):
                st.warning(f"📌 {c}")
        else:
            st.success("🎉 Comprehensive coverage! Recommended for ACC Fast-Track Mock Placement Drive.")

    # Deep-dive Skill Badges
    st.markdown("#### 🔍 Detailed Keyword Breakdown")
    for category, data in results.items():
        with st.expander(f"{category} — {len(data['found'])} Found / {len(data['missing'])} Missing", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Found in Resume:**")
                if data["found"]:
                    badges = "".join([f'<span class="badge-found">✓ {kw}</span>' for kw in data["found"]])
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.write("No matching tools detected.")
            with c2:
                st.write("**Missing / Gaps:**")
                if data["missing"]:
                    badges = "".join([f'<span class="badge-missing">✕ {kw}</span>' for kw in data["missing"]])
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.write("Zero gaps in this category!")

    # Mentor Consultation & Automated Session Arrangement Section
    st.markdown("""
    <div class="mentor-card">
        <h3 style="margin-top:0; color:#58a6ff;">🎯 Free 1-on-1 Mentor Consultation & Session Arrangements</h3>
        <p style="color:#c9d1d9;">Book an instant 1-on-1 resume audit and career roadmapping session directly with an ACC Senior Analytics Mentor.</p>
        <p>Direct Support & Session Desk: <b style="color:#79c0ff;">internships@analyticscareerconnect.com</b> | <b style="color:#79c0ff;">+91 94038 12709</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    col_form, col_quick = st.columns([1.6, 1.4], gap="medium")

    with col_form:
        with st.form("mentor_lead_capture"):
            st.write("**Candidate Session Details**")
            name = st.text_input("Your Full Name")
            email = st.text_input("Your Email Address")
            phone = st.text_input("WhatsApp / Contact Number")
            notes = st.text_area("Preferred Time / Target Companies (optional):", height=70)
            submit = st.form_submit_button("Book Free Session with ACC Mentor", use_container_width=True)

            if submit:
                if name and (email or phone):
                    st.session_state["booked"] = True
                    st.session_state["book_name"] = name
                    st.session_state["book_phone"] = phone
                    st.session_state["book_email"] = email
                    st.session_state["book_notes"] = notes
                else:
                    st.warning("Please provide your name along with an email or phone number to proceed.")

    with col_quick:
        if st.session_state.get("booked", False):
            b_name = st.session_state["book_name"]
            b_phone = st.session_state["book_phone"]
            b_email = st.session_state["book_email"]
            b_notes = st.session_state.get("book_notes", "None")

            st.success(f"✅ Session Request Generated for **{b_name}**!")

            st.markdown(f"""
            **Automated Session Arrangements:**
            * **Assigned Mentor Desk:** HR department ACC
            * **Official Contact:** `+91 94038 12709`
            * **Mentor Email:** `internships@analyticscareerconnect.com`
            * **ATS Match Score:** `{score}%` for *{selected_role}*
            * **Session Mode:** 1-on-1 Google Meet / WhatsApp Call
            * **Arrangement Status:** Ready to Confirm
            """)

            # Automated WhatsApp Direct Message URL
            wa_message = (
                f"Hi HR Department ACC,%0A%0A"
                f"I would like to confirm my Free 1-on-1 Mentor Consultation!%0A"
                f"- Name: {b_name}%0A"
                f"- Target Role: {selected_role}%0A"
                f"- ATS Match Score: {score}%%0A"
                f"- Phone: {b_phone}%0A"
                f"- Email: {b_email}%0A"
                f"- Note: {b_notes}%0A%0A"
                f"Please share the available meeting slots."
            )
            wa_url = f"https://api.whatsapp.com/send?phone=919403812709&text={wa_message}"

            st.link_button(
                "💬 Open WhatsApp to Lock In Slot (+91 94038 12709)",
                wa_url,
                type="primary",
                use_container_width=True
            )
        else:
            st.write("**Direct Mentor Connect**")
            st.info("Fill out your details on the left and click **Book Free Session** to automatically route your request to the mentor desk via WhatsApp or Email.")
            
            mailto_link = f"mailto:internships@analyticscareerconnect.com?subject=ACC%20Resume%20Review%20Request%20-%20{selected_role}&body=Hi%20HR%20Department%20ACC,%0D%0A%0D%0AI%20scanned%20my%20resume%20for%20the%20{selected_role}%20role%20and%20scored%20{score}%.%20I%20would%20like%20to%20schedule%20a%20free%20consultation."
            st.link_button("✉️ Send Direct Email to Desk", mailto_link, use_container_width=True)