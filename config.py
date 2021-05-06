import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Connect to the database
DATABASE_URI = os.path.join(basedir, 'database.db')

# Runner config
MAX_RESULTS = 50
SEARCH_QUERY = os.environ.get('YT_QUERY') or 'official'
FETCH_FREQ = 10  # In seconds

# Log path
RUNNER_LOG = os.path.join(os.path.join(basedir, 'logs'), 'yt-runner.log')
APP_LOG = os.path.join(os.path.join(basedir, 'logs'), 'yt-api.log')
