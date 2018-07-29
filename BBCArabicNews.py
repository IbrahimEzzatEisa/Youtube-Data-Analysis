
import argparse
import csv
import unidecode
from apiclient.discovery import build
from apiclient.errors import HttpError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


DEVELOPER_KEY = "AIzaSyAohpXhbmOVWcyEv4VLs5GWLcp_5M-nhfU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.max_results).execute()


    channels = []



    csvFile = open('Channel_result.csv', 'w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow([ "subscribe", "viewCount", "likeCount", "dislikeCount", "commentCount"])

  ##
    for search_result in search_response.get("items", []):

        if search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))


    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            # videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId, part="statistics").execute()
            for video_result in video_response.get("items", []):
                if 'likeCount' not in video_result["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_result["statistics"]["commentCount"]
                if 'subscribe' not in video_result["statistics"]:
                    subscribeCount = 0
                else:
                    subscribeCount = video_result["statistics"]["subscribe"]
                if 'viewCount' not in video_result["statistics"]:
                     viewCount = 0
                else:
                     viewCount = video_result["statistics"]["viewCount"]

            csvWriter.writerow([viewCount, likeCount, dislikeCount, commentCount, subscribeCount])


    csvFile.close()
    print(" BBC News عربي")
    youtube_data = pd.read_csv('Channel_result.csv')

    print(youtube_data)

    print("Channels:\n", "\n".join(channels), "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='like')
    parser.add_argument("--q", help="Search term", default="bbcarabicnews")
    parser.add_argument("--max-results", help="Max results", default=25)
    args = parser.parse_args()
    try:
     youtube_search(args)
    except HttpError.e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

