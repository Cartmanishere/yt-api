# Youtube API

This is toy example of working with youtube API to fetch video data
and serving it using an API.

There are two components in this project.
1. Youtube Runner
2. API to fetch data

## Run

To run this project, you need to have `Python 3.8` or above installed.

1. Install dependencies
```
pip install requirements.txt
```

2. Start the components
```
# For runner
export YT_API_KEY='xxxx'
python runner.py
# logs are present in logs/yt-runner.log

# For API
python app.py
# logs are present in logs/yt-api.log
```

3. Wait until the runner inserts some data into database.
4. Visit `https://localhost:5000/videos`

## Youtube Runner

This component runs in a loop to query the youtube search API to find videos
related to a particular search term.

This search term can be configured in the `config.py` file.

Or this seach term can be set using the environement variable --
```
export YT_SEARCH='official'
```

You also need to provide an API key with Youtube API V3 access as follows --
```
export YT_API_KEY='xxxx'
```

## API

It is a flask API to fetch the video information. There are two routes in this API as follows --

### Get videos

#### Request
```
GET /videos

Supported Query Params:
num [int] -> number of results to return in response.
after [str] -> Datetime in isoformat for pagination.
```

#### Response

Example --
```
{
    "data": [
        {
            "channel_id": "UC-rPEnjVmDAmLpUJukl6jMw",
            "created_at": "Thu, 06 May 2021 14:14:51 GMT",
            "description": "",
            "id": "_0b9wC_DROg",
            "published_at": "2021-05-06 08:27:11+00:00",
            "title": "AtomyIndia Official Live Stream"
        },
    ],
    "msg": "",
    "success": true
}
```

### Search videos

#### Request
```
GET /videos/search

Supported Query Params:
query [str] (required) -> search term
num [int] -> number of results to return in response.
after [str] -> Datetime in isoformat for pagination.
```

#### Response

Example --
```
{
    "data": [
        {
            "channel_id": "UC-rPEnjVmDAmLpUJukl6jMw",
            "created_at": "Thu, 06 May 2021 14:14:51 GMT",
            "description": "",
            "id": "_0b9wC_DROg",
            "published_at": "2021-05-06 08:27:11+00:00",
            "title": "AtomyIndia Official Live Stream"
        },
    ],
    "msg": "",
    "success": true
}
```

## Database

SQlite database is used for storing the youtube video information.

Peewee ORM is used for handling interaction with the database.

## Docker

### Usage

1. Build the docker image
```
docker build -t yt-api .
```

2. Run the image
```
docker run -p 5000:5000 -e YT_API_KEY='xxxx' -e YT_SEARCH='official' yt-api
```

3. Check the API
   - Visit `http://localhost:3000/videos` to check the videos.
   - Note: It will take the Youtube Runner component 10-15 seconds to populate the database.

### Troubleshoot

If you do not see any data appearing in the repsonse, it is worth checking whether there was an error in runner.

This can be debugged by accessing the respective logs. Here's how to do it --

1. Get the docker container name
```
docker ps
# This should return you the name of the docker container
```

2. Go inside the container and check the logs
```
a. docker exec -it <container-name> /bin/bash
b. tail -f logs/yt-api.log
or
b. tail -f logs/yt-runner.log
```
