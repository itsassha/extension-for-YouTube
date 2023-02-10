import pandas as pd
import gspread
import requests
import json
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

def get_comments(video_id):
    # Авториазция токена YouTube
    api_key = "YouTube_api_key"
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        for item in data["items"]:
            comment = {
                "author": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                "text": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
            }
            comments.append(comment)
    return comments

def upload_comments(comments, spreadsheet_id):
    # Авторизация учетной записи
    credentials = Credentials.from_service_account_file("path/to/service_account.json")
    gc = gspread.authorize(credentials)
    # Таблица Google Sheets
    sh = gc.open_by_key(spreadsheet_id)
    # Фрейм данных из комментариев
    df = pd.DataFrame(comments)
    # Очиста листа
    worksheet = sh.sheet1
    worksheet.clear()
    # Загрузка листа
    set_with_dataframe(worksheet, df)

if __name__ == "__main__":
    video_id = "abc123"
    comments = get_comments(video_id)
    spreadsheet_id = "spreadsheet_id"
    upload_comments(comments, spreadsheet_id)
