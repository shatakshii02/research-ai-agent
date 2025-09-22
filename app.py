import streamlit as st
from db_util import get_all_reports, get_report
from agent import generate_report
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="wide")
st.title("🔎 AI Research Agent — Query → Search → Extract → Summarize → Save")

with st.sidebar:
    st.header("📜 Past Reports")
    reports = get_all_reports()
    if not reports:
        st.info("No reports yet. Run your first query!")
    else:
        # list in sidebar and allow selection
        labels = [f"#{r['id']} • {r['query'][:60]} • {r['created_at']}" for r in reports]
        sel = st.selectbox("Open a report:", options=["(select)"] + labels, index=0)
        if sel != "(select)":
            try:
                rid = int(sel.split("•")[0].replace("#","").strip())
                r = get_report(rid)
                if r:
                    st.subheader("Opened Report")
                    st.write(f"**Query:** {r['query']}")
                    st.markdown(r["summary"], unsafe_allow_html=True)
            except Exception:
                st.warning("Could not open that report.")

st.subheader("🧪 New Query")
query = st.text_input("Enter your research question", placeholder="e.g., Impact of Mediterranean diet on heart health")
go = st.button("Generate Report", type="primary")

if go:
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching, extracting, and summarizing..."):
            summary = generate_report(query.strip())
        st.success("Done!")
        st.markdown(summary, unsafe_allow_html=True)

st.caption("Built with Groq Llama3, SerpAPI, Trafilatura, PyPDF, and SQLite.")