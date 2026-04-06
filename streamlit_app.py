import streamlit as st
import requests

@st.cache_data
def fetch_reports():
    response = requests.get("http://localhost:8000/reports")
    return response.json()

st.title("News Analyst Agent")

# Sidebar — past reports

# Main - research input
goal = st.text_input("Research a topic")

if st.button("Submit"):
    st.cache_data.clear()
    with st.spinner("Thinking..."):
        response = requests.post("http://localhost:8000/research", json={"goal": goal})
    report = response.json()    
    st.header(report["goal"])
    st.write(report["conclusion"])
    for p in report["perspectives"]:
        st.write(f"**{p['name']}**: {p['summary']}")
    for s in report["sources"]:
        st.markdown(f"[{s['title']}]({s['url']})")

with st.expander("Past Records"):
    reports = fetch_reports()   
    for report in reports:
        with st.expander(report["goal"]):
            st.header(report["goal"])
            st.write(report["conclusion"])
            for p in report["perspectives"]:
                st.write(f"**{p['name']}**: {p['summary']}")
            for s in report["sources"]:
                st.markdown(f"[{s['title']}]({s['url']})")