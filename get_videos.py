
import os
import requests
from html import unescape
from pymongo import MongoClient
import dateutil.parser

conn = MongoClient("localhost", 27017)
db = conn.get_database("nl_words")
coll = db.get_collection("videos")

req_url = "https://www.googleapis.com/youtube/v3/playlistItems"
yt_key = os.getenv("YT_KEY")


items = []
cont = True
next_page = None
count = 1

while cont:
    if next_page:
        params = {
            "part": "snippet",
            "key": yt_key,
            "playlistId": "[PLAYLIST ID]",
            "maxResults": 50,
            "pageToken": next_page,
        }
    else:
        params = {
            "part": "snippet",
            "key": yt_key,
            "playlistId": "[PLAYLIST ID]",
            "maxResults": 50,
        }

    print("Gathering")
    results = requests.get(req_url, params=params)

    if results.json().get("items"):
        items = results.json().get("items")

        for item in items:
            if not coll.count_documents({"video_id": item["snippet"]["resourceId"]["videoId"]}):
                doc = {
                    "date": dateutil.parser.parse(item["snippet"]["publishedAt"]),
                    "title": unescape(item["snippet"]["title"]),
                    "video_id": item["snippet"]["resourceId"]["videoId"]
                }

                coll.insert_one(doc)
                print(f"Inserted: {count}")
                count += 1
            else:
                print("Duplicate")

    next_page = results.json().get("nextPageToken")
    print(next_page)

    if not next_page:
        print("Done")
        cont = False


