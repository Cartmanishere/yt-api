import datetime
from playhouse.shortcuts import model_to_dict
from db.models import Video
from dateutil.parser import parse


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

