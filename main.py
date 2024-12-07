import streamlit as st
import intro
import experiment
import complete

# Streamlit 페이지 구성
st.set_page_config(layout="wide", page_title="ReadingAssistantExperiment", page_icon="🌟")

# 페이지 전환
if "page" not in st.session_state:
    st.session_state["page"] = "intro"
    
if st.session_state["page"] == "intro":
    intro.intro_page()
elif st.session_state["page"] == "experiment":
    experiment.experiment_page()
elif st.session_state["page"] == "completion":
    complete.completion_page()