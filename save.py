import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets():
    # 인증 정보 설정
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('readingassistant-443805-96a3c0a0c22a.json', scope)
    client = gspread.authorize(credentials)
    
    # 구글 스프레드시트 열기 (스프레드시트 이름 변경 필요)
    spreadsheet = client.open("ReadingAssistant").sheet1
    return spreadsheet

def record_to_sheets(response_data):
    spreadsheet = authenticate_google_sheets()
    spreadsheet.append_row(response_data)
