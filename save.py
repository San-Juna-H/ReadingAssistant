import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def authenticate_google_sheets():
    # Streamlit Secrets에서 JSON 인증 정보 가져오기
    api_key = st.secrets["google_cloud"]["api_key"]
    
    # api_key가 멀티라인 문자열로 되어 있을 수 있기 때문에 처리
    try:
        # JSON 문자열로 변환
        credentials_dict = json.loads(api_key)
    except json.decoder.JSONDecodeError as e:
        st.error(f"JSON Decode Error: {e}")
        return None
    
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