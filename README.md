 ACC Resume ATS & Skill-Gap Scanner

An interactive AI-powered application designed for **Analytics Career Connect (ACC)** to evaluate candidate resumes against industry-standard data and business analytics benchmarks, identify missing technical skills, and automate career mentorship bookings.

---

Key Features

- Automated Text Extraction: Parses text directly from uploaded `.pdf`, `.docx`, or raw text inputs.
- ATS Compatibility Scoring: Computes an immediate percentage match based on target roles:
  - Data Analyst: Evaluates SQL, BI/Visualization (Power BI, Tableau), Python (Pandas, NumPy, EDA), and Statistical Analysis.
  - Business Analyst: Evaluates BRD/FRD requirements, Agile/Scrum methodologies, KPI tracking, and Stakeholder Management.
- Visual Performance Analytics: 
  - Dynamic horizontal competency coverage bar chart.
  - Color-coded badge pills distinguishing identified skills vs. critical skill gaps.
- ACC Bridge Recommendations: Dynamically links identified skill gaps to relevant ACC training masterclasses and bootcamps.
- Lead Capture & Direct Routing:
  - One-click session arrangement interface.
  - Automated WhatsApp pre-filled booking via `+91 94038 12709`.
  - Direct email routing to `internships@analyticscareerconnect.com`.

---

 🛠️ Tech Stack

- Frontend & App Framework: [Streamlit](https://streamlit.io/)
- Data Processing: Python, Pandas
- Document Parsing: `pdfplumber`, `python-docx`
- Pattern Matching: Regular Expressions (`re`)

---

 📂 Project Structure

```text
├── app.py                # Main Streamlit application and dashboard UI
├── parser.py             # Document extraction and keyword parsing algorithms
├── skills_data.py        # Core skill taxonomies and course recommendation mappings
├── requirements.txt      # Python dependencies for deployment
└── README.md             # Project documentation
