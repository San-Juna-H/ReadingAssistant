import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets():

    credentials_dict = {
        "type": f"{st.secrets["type"]}",
        "project_id": f"{st.secrets["project_id"]}",
        "private_key_id": f"{st.secrets["private_key_id"]}",
        "private_key": f"{st.secrets["private_key"]}",
        "client_email": f"{st.secrets["client_email"]}",
        "client_id": f"{st.secrets["client_id"]}",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"{st.secrets["client_x509_cert_url"]}",
        "universe_domain": "googleapis.com"
    }
    
    st.write(credentials_dict)
    
    # 인증 정보 설정
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(credentials)
    
    # 구글 스프레드시트 열기 (스프레드시트 이름 변경 필요)
    spreadsheet = client.open("ReadingAssistant").sheet1
    return spreadsheet

def record_to_sheets(response_data):
    spreadsheet = authenticate_google_sheets()
    # 첫 번째 행에 데이터를 삽입
    spreadsheet.insert_row(response_data, 3)