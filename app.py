import streamlit as st
import requests
import pandas as pd

st.title("Supply Chain Scenario Analysis")

uploaded_file = st.file_uploader("Upload Supply Chain Excel", type=["xlsx"])

if uploaded_file is not None:
    if st.button("Analyze"):
        files = {"file": (uploaded_file.name, uploaded_file, "application/vnd.ms-excel")}
        response = requests.post("http://localhost:8000/analyze", files=files)

        if response.status_code == 200:
            analysis = response.json().get("analysis")
            st.write("### Scenario Analysis Results")
            st.write(analysis)
        else:
            st.error("Failed to retrieve analysis")
