#!/usr/bin/env python3

import argparse
import queue
import sys
import time
import threading

import flask
import spotipy
import spotipy.util

app = flask.Flask(__name__)

queue = queue.Queue()


exiting = False
sp = None


@app.route('/', methods=['GET'])
def get_index():
    return flask.render_template('index.html')

@app.route('/', methods=['POST'])
def post_index():
    uri = flask.request.form.get('spotify_uri')
    track = sp.track(uri)
    duration = float(track['duration_ms']) / 1000

    queue.put_nowait((uri, duration - 2))

    print(f'current queue size: {queue.unfinished_tasks}')

    return flask.redirect('/')

@app.route('/debug')
def debug():
    import pdb
    pdb.set_trace()
    return flask.redirect('/')

def process_queue():
    while not exiting:
        uri, duration = queue.get()

        print(f'retrieved {uri} from queue, starting playback')
        sp.start_playback(uris=[uri])

        print(f'sleeping for {duration}')
        time.sleep(duration)
        queue.task_done()

        print(f'current queue size: {queue.unfinished_tasks}')

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('username')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000)

    return parser.parse_args()

def main():
    global exiting
    global sp

    args = parse_args()

    token = spotipy.util.prompt_for_user_token(
        args.username,
        'user-modify-playback-state',
    )

    sp = spotipy.Spotify(auth=token)

    process_queue_thread = threading.Thread(target=process_queue)
    process_queue_thread.start()

    try:
        app.run(host=args.host, port=args.port)
    except KeyboardInterrupt:
        exiting = True

    process_queue_thread.join(timeout=10)

    return True

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
