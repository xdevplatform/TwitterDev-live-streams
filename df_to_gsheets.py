import pandas as pd
import gspread
import os
import requests

from oauth2client.service_account import ServiceAccountCredentials


def connect_to_twitter():
    bearer_token = os.environ.get('BEARER_TOKEN')
    return {"Authorization": "Bearer {}".format(bearer_token)}
    

def make_request(headers):
    # Will use timelines if available 
    url = "https://api.twitter.com/2/tweets/search/recent?query=from:TwitterDev"
    return requests.request("GET", url, headers=headers).json()


def make_df(response):
    return pd.DataFrame(response['data'])


def authenticate_to_google():
    scope = [
        "https://spreadsheets.google.com/feeds"
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "path/to/my/file.json", scope
    )
    return credentials


def main():
    headers = connect_to_twitter()
    response = make_request(headers)
    df = make_df(response)
    credentials = authenticate_to_google()
    gc = gspread.authorize(credentials)
    # will likely use an env vairable for the but may switch over to a configuration if it's easier
    workbook = gc.open_by_key('google-sheets-key')
    sheet = workbook.worksheet('recent_search_results')
    sheet.update('A1', [df.columns.values.tolist()] + df.values.tolist())


if __name__ == "__main__":
    main()
