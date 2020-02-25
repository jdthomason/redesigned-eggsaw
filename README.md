# Egg Words Quasi-Analyzer

Nothing too fancy happening here.  Just a small side project.

Things required:

1. MongoDB.  Docker compose file included.
2. Python 3.6.8
3. Packages given in `requirements.txt`

Operating:

1. `get_videos.py` is what obtains video IDs from the YouTube API.  The correct endpoint is given but operation requires an API key in your environment variables.
2. `get_transcripts.py` is what does the heavy lifting in obtaining the video transcripts and word counts.  Should just require a button push once you've got the videos.
3. `nl_words_analysis.ipynb` is a Jupyter Notebook with various analysis things.
4. `Stop_Words.txt` is a large list of stop words to combine with whatever is already in `NLTK`.