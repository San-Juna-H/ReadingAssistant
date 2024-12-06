import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets():

    # Streamlit Secrets에서 JSON 인증 정보 가져오기
    api_key = st.secrets["api_key"]
    st.write(api_key)


    # 줄바꿈 문자를 실제 줄바꿈으로 변환
    api_key = api_key.replace(" ", "\n")
    
    
    credentials_dict = json.loads(api_key)
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