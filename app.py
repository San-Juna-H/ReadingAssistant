import streamlit as st
import pages
import data
import save
import pandas as pd

# Streamlit 페이지 구성
st.set_page_config(page_title="전문 용어 이해 실험", layout="wide")

# 페이지 전환
if "page" not in st.session_state:
    st.session_state["page"] = "intro"

if st.session_state["page"] == "intro":
    pages.intro_page()
elif st.session_state["page"] == "experiment":
    pages.experiment_page()
elif st.session_state["page"] == "completion":
    pages.completion_page()