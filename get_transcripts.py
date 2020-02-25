from pymongo import MongoClient
from youtube_transcript_api import YouTubeTranscriptApi

conn = MongoClient("localhost", 27017)
db = conn.get_database("nl_words")
videos_coll = db.get_collection("videos")

videos = list(videos_coll.find({}))

transcripts = []
count = 1

for video in videos:
    m_id = video["_id"]
    vid_id = video["video_id"]
    title = video["title"]
    date = video["date"]

    if not video.get("time_min"):
        words = []
        time = None

        try:
            trans = YouTubeTranscriptApi.get_transcript(vid_id)

            for line in trans:
                words.extend(line["text"].split(" "))

            time = round(max(x["start"] for x in trans) / 60)
        except Exception:
            pass

        if len(words) > 0:
            doc = {
                "text": " ".join(words),
                "words": words,
                "word_count": len(words),
                "time_min": time
            }
        else:
            doc = {
                "text": None,
                "words": None,
                "word_count": None,
                "time_min": None
            }
        print(f"Inserting: {count}")
        videos_coll.update_one({"_id": m_id}, {"$set": doc})
        count += 1
    else:
        print("Duplicate or no transcript")
print("Done")
