import datetime
from playhouse.shortcuts import model_to_dict
from db.models import Video
from dateutil.parser import parse

DEFAULT_MAX_RESULTS = 10


def add_video(video):
    """
    Adds a video to the database. If the video with same id already,
    exists, then it does not create a new video.
    :param video: details of the video.
    :return video: video created in the db.
    :return created: whether video was created or not.
    """
    video, created = Video.get_or_create(
        id=video['id'],
        channel_id=video['channel_id'],
        title=video['title'],
        description=video['description'],
        published_at=parse(video['published_at'])
    )
    return video, created


def get_video(video_id):
    """
    Get the video using the id.
    :param video_id: id of the video.
    :return video: Video data.
    """
    return Video.get_by_id(video_id)


def get_videos_desc(cursor=None, max_results=None):
    """
    Fetch videos in descending order based on published_at.
    :param cursor: A datetime obj to fetch next set of results for pagination.
    :param max_results: Max number of results to return.
    :return: a list of videos.
    """
    if not cursor:
        cursor = datetime.datetime.now()

    if not max_results:
        max_results = DEFAULT_MAX_RESULTS

    res = Video.select().where(Video.published_at < cursor) \
               .order_by(Video.published_at.desc()).limit(max_results)

    return [model_to_dict(video) for video in res]


def video_search(query, cursor=None, max_results=None):
    """
    Search video based on query string. Match using the title of
    the video.
    :param query: Search query
    :param cursor: A datetime obj to fetch next set of results for pagination.
    :param max_results: Max number of results to return.
    :return: a list of videos.
    """
    if not cursor:
        cursor = datetime.datetime.now()

    if not max_results:
        max_results = DEFAULT_MAX_RESULTS

    exp = ((Video.title.contains(query)) | (Video.description.contains(query))) \
            & (Video.published_at < cursor)
    res = Video.select().where(exp) \
               .order_by(Video.published_at.desc()).limit(max_results)

    return [model_to_dict(video) for video in res]




