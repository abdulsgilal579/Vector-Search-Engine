import streamlit as st
import requests 

API_URL = "http://127.0.0.1:8000"

st.title("UPLOAD PDF AND INGEST IT")

upload_tab, ask_tab = st.tabs(["Upload PDF", "ASK Questions"])

with upload_tab:
    uploaded_file = st.file_uploader("Upload PDF Here")

    if uploaded_file and st.button("Ingest It"):
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        response = requests.post(f"{API_URL}/ingest", params={"file_path": uploaded_file.name})
        st.write(response.json()["Source"])

with ask_tab:
    query = st.chat_input("Ask question here")
    if query:
        resposne = requests.get(f"{API_URL}/ask", params={"q": query, "limit": 1})
        st.write(resposne.json()["Lmm Result: "])