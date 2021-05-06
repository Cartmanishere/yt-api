from flask import Flask, jsonify, request
import logging
import os
from config import APP_LOG
from db.handlers import get_videos_desc, video_search
from db.models import init
from dateutil.parser import parse

logging.basicConfig(filename=APP_LOG,
                    format='[%(asctime)s] [YT-APP] %(levelname)s %(message)s')

# Initialize db
init()
app = Flask(__name__)


def json_response(data, status_code=200, msg=''):
    return {
        'success': status_code == 200,
        'msg': msg,
        'data': data
    }, status_code


@app.route('/ping')
def test():
    return 'pong'


@app.route('/videos')
def get_videos():
    dt = request.args.get('after')
    cursor = None
    if dt:
        try:
            cursor = parse(dt)
        except Exception as e:
            return json_response([],
                                 msg='Invalid cursor format',
                                 status_code=400)

    max_results = request.args.get('num')
    return json_response(get_videos_desc(cursor, max_results))


@app.route('/videos/search')
def search():
    query = request.args.get('query')
    if not query:
        return json_response([], msg='query is an required field', status_code=400)

    dt = request.args.get('after')
    cursor = None
    if dt:
        try:
            cursor = parse(dt)
        except Exception as e:
            return json_response([],
                                 msg='Invalid cursor format',
                                 status_code=400)
    max_results = request.args.get('num')
    return json_response(video_search(query,
                                      cursor=cursor,
                                      max_results=max_results))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
