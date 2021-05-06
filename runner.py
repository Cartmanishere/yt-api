import datetime
import time
import pytz
from yt import YoutubeSearch
from db.handlers import add_video
from db.models import init, RunnerMeta
from config import SEARCH_QUERY, MAX_RESULTS, FETCH_FREQ
from config import RUNNER_LOG
from googleapiclient.errors import HttpError
import logging

logging.basicConfig(filename=RUNNER_LOG,
                    format='[%(asctime)s] [YT-RUNNER] %(levelname)s %(message)s',
                    level=logging.INFO)


class YoutubeRunner:
    def __init__(self):
        self.yt = YoutubeSearch()
        # Initialize the database conn
        init()
        # Start the runner
        logging.info('Initialized the YT-RUNNER')
        self.last_fetch = time.time()
        # Initialize db state to track last run
        self.meta, _ = RunnerMeta.get_or_create(id='yt-runner')

    def fetch_videos(self):
        """
        Fetch videos from the YT API and save them in the database.
        """
        published_after = self.meta.last_run

        while True:
            cur_time = time.time()
            if cur_time - self.last_fetch < FETCH_FREQ:
                continue

            logging.info(f'Querying videos after: {published_after.isoformat()}')
            videos = []
            try:
                videos = self.yt.search(SEARCH_QUERY,
                                        published_after.replace(tzinfo=pytz.UTC).isoformat(),
                                        MAX_RESULTS)
            except HttpError as e:
                logging.error(e)

            n = 0
            for video in videos:
                _, created = add_video(video)
                if created:
                    n += 1

            self.last_fetch = cur_time
            published_after = datetime.datetime.now()
            self.meta.last_run = published_after
            self.meta.save()

            logging.info(f'Saved {n} videos into database')


if __name__ == "__main__":
    YoutubeRunner().fetch_videos()
