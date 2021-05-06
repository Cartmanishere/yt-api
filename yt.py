from googleapiclient.discovery import build
import logging
import os


class YoutubeSearch:
    def __init__(self):
        """
        Initialize the youtube client for doing the search queries.
        """
        try:
            os.environ['YT_API_KEY']
        except KeyError as e:
            logging.error('YT_API_KEY not found in environment')
            exit(1)

        self.youtube = build('youtube', 'v3',
                             developerKey=os.environ['YT_API_KEY'],
                             cache_discovery=False)

    @staticmethod
    def massage(id, snippet):
        return {
            'id': id['videoId'],
            'published_at': snippet['publishedAt'],
            'channel_id': snippet['channelId'],
            'title': snippet['title'],
            'description': snippet['description'],
        }

    def search(self, query, published_after=None, max_results=5):
        """
        Search youtube videos for some search query.
        :param query: Search term to query.
        :param published_after: datetime for searching videos after that date.
        :param max_results: No. of results to fetch.
        :return:
        """
        search_response = self.youtube.search().list(q=query,
                                                     part='id,snippet',
                                                     maxResults=max_results,
                                                     type='video',
                                                     publishedAfter=published_after).execute()

        videos = map(lambda x: YoutubeSearch.massage(x['id'], x['snippet']), search_response['items'])
        return list(videos)
