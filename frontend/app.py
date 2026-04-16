import streamlit as st
import requests
import pandas as pd
import os

API_BASE = "http://localhost:3000"  # change if deployed

st.set_page_config(page_title="PDF Processor", layout="wide")

st.title("📄 PDF Upload & CSV Extractor")

# -----------------------------
# Upload Section
# -----------------------------
st.header("Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.button("Upload & Process"):
        with st.spinner("Processing..."):

            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{API_BASE}/upload/", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success("Upload successful!")

            st.json(data)

            base_name = uploaded_file.name.replace(".pdf", "")

            items_url = f"{API_BASE}/download/items/{uploaded_file.name}"
            buildings_url = f"{API_BASE}/download/buildings/{uploaded_file.name}"

            # -----------------------------
            # Load CSVs
            # -----------------------------
            st.header("📊 Extracted Data")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Items Table")
                try:
                    items_df = pd.read_csv(items_url)
                    st.dataframe(items_df, width="stretch")

                    st.download_button(
                        "⬇️ Download Items CSV",
                        data=items_df.to_csv(index=False),
                        file_name=f"{base_name}_items.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.warning("Items CSV not found yet.")

            with col2:
                st.subheader("Buildings Table")
                try:
                    buildings_df = pd.read_csv(buildings_url)
                    st.dataframe(buildings_df, width="stretch")

                    st.download_button(
                        "⬇️ Download Buildings CSV",
                        data=buildings_df.to_csv(index=False),
                        file_name=f"{base_name}_buildings.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.warning("Buildings CSV not found yet.")

        else:
            st.error(f"Upload failed: {response.text}")