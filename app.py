#!/usr/bin/env python3

import argparse
import datetime
import queue
import sys
import time
import threading

import flask
import spotipy
import spotipy.util

app = flask.Flask('spockify')

queue = queue.Queue()


exiting = False
sp = None


@app.route('/', methods=['GET'])
def get_index():
    return flask.render_template('index.html', queue=queue.queue, errors=[])

@app.route('/', methods=['POST'])
def post_index():
    errors = []

    uri = flask.request.form.get('spotify_uri')

    try:
        track = sp.track(uri)
    except spotipy.client.SpotifyException as e:
        app.logger.error(f'received error from spotify: {str(e)}')
        errors.append(str(e))
    else:
        track['artist'] = ', '.join(artist['name'] for artist in track['artists'])

        duration = datetime.timedelta(milliseconds=track['duration_ms'])

        track['duration'] = '{:02d}:{:02d}'.format(
            (duration.seconds % 3600) // 60,
            duration.seconds % 60,
        )

        duration = float(track['duration_ms']) / 1000

        queue.put_nowait((track, duration - 2))

        app.logger.debug(f'current queue size: {queue.unfinished_tasks}')

    return flask.render_template('index.html', queue=queue.queue, errors=errors)

@app.route('/debug')
def debug():
    import pdb
    pdb.set_trace()
    return flask.redirect('/')

def process_queue():
    while not exiting:
        track, duration = queue.get()

        app.logger.debug(f'retrieved {track["uri"]} from queue, starting playback')
        sp.start_playback(uris=[track['uri']])

        app.logger.debug(f'sleeping for {duration}')
        time.sleep(duration)
        queue.task_done()

        app.logger.debug(f'current queue size: {queue.unfinished_tasks}')

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('username')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000)
    parser.add_argument('--debug', action='store_true')

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
        app.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        exiting = True

    process_queue_thread.join(timeout=10)

    return True

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
