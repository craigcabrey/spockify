#!/usr/bin/env python3

import argparse
import datetime
import json
import queue
import os
import sys
import time
import threading

import flask
from flask_cors import CORS
import spotipy
import spotipy.oauth2
import spotipy.util

app = flask.Flask('spockify')

queue = queue.Queue()
exiting = False
sp = None


class Track:

    @classmethod
    def from_id(cls, id):
        return cls(sp.track(id))

    def __init__(self, metadata):
        self._metadata = metadata

    @property
    def human_duration(self):
        duration = datetime.timedelta(milliseconds=self._metadata['duration_ms'])

        return '{:02d}:{:02d}'.format(
            (duration.seconds % 3600) // 60,
            duration.seconds % 60,
        )

@app.route('/api/', methods=['GET'])
def api_get_index():
    errors = []
    now_playing_track = sp.current_playback()

    if now_playing_track:
        now_playing_track['artist'] = ', '.join(
            artist['name'] for artist in now_playing_track['item']['artists']
        )

        for image in now_playing_track['item']['album']['images']:
            if image['height'] == 300:
                now_playing_track['album_art_url'] = image['url']
    ret = {
        'now_playing': now_playing_track,
        'queue': list(queue.queue),
        'errors': errors,
    }
    return flask.jsonify(ret)

@app.route('/api/', methods=['POST'])
def api_post_index():
    errors = []
    uri = flask.request.get_json()
    print(uri)
    uri = uri['spotify_uri']

    *_, uri_type, _ = uri.split(':')

    if 'http' in uri_type:
        # given a url, so split by '/'
        *_, uri_type, _ = uri.split('/')

    try:
        tracks = globals()[f'handle_{uri_type}_uri'](uri)
    except spotipy.client.SpotifyException as e:
        app.logger.error(f'received error from spotify: {str(e)}')
        errors.append(str(e))
    else:
        for track in tracks:
            track['artist'] = ', '.join(artist['name'] for artist in track['artists'])

            duration = datetime.timedelta(milliseconds=track['duration_ms'])

            track['duration'] = '{:02d}:{:02d}'.format(
                (duration.seconds % 3600) // 60,
                duration.seconds % 60,
            )

            duration = float(track['duration_ms']) / 1000

            queue.put_nowait((track, duration - 2))

        app.logger.debug(f'current queue size: {queue.unfinished_tasks}')
    ret = {}
    if errors:
        ret ['success'] = 0
        ret['errors'] = errors
    else:
        ret ['success'] = 1
        ret['queue'] = list(queue.queue)
    
    return flask.jsonify(ret)


@app.route('/', methods=['GET'])
def get_index():
    now_playing_track = sp.current_playback()

    if now_playing_track:
        now_playing_track['artist'] = ', '.join(
            artist['name'] for artist in now_playing_track['item']['artists']
        )

        for image in now_playing_track['item']['album']['images']:
            if image['height'] == 300:
                now_playing_track['album_art_url'] = image['url']

    return flask.render_template(
        'index.html',
        now_playing=now_playing_track,
        queue=queue.queue,
        errors=[],
    )

def handle_playlist_uri(uri):
    for item in sp.user_playlist(user=None, playlist_id=uri)['tracks']['items']:
        yield item['track']

def handle_track_uri(uri):
    yield sp.track(uri)

@app.route('/', methods=['POST'])
def post_index():
    errors = []

    uri = flask.request.form.get('spotify_uri')

    *_, uri_type, _ = uri.split(':')

    if 'http' in uri_type:
        # given a url, so split by '/'
        *_, uri_type, _ = uri.split('/')

    try:
        tracks = globals()[f'handle_{uri_type}_uri'](uri)
    except spotipy.client.SpotifyException as e:
        app.logger.error(f'received error from spotify: {str(e)}')
        errors.append(str(e))
    else:
        for track in tracks:
            track['artist'] = ', '.join(artist['name'] for artist in track['artists'])

            duration = datetime.timedelta(milliseconds=track['duration_ms'])

            track['duration'] = '{:02d}:{:02d}'.format(
                (duration.seconds % 3600) // 60,
                duration.seconds % 60,
            )

            duration = float(track['duration_ms']) / 1000

            queue.put_nowait((track, duration - 2))

        app.logger.debug(f'current queue size: {queue.unfinished_tasks}')

    if errors:
        return flask.render_template('index.html', queue=queue.queue, errors=errors)
    else:
        return flask.redirect(flask.url_for('get_index'))

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

    parser.add_argument('--client-id', default=os.getenv('SPOCKIFY_CLIENT_ID'))
    parser.add_argument('--client-secret', default=os.getenv('SPOCKIFY_CLIENT_SECRET'))
    parser.add_argument('--redirect-uri', default=os.getenv('SPOCKIFY_REDIRECT_URI'))
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000)
    parser.add_argument('--debug', action='store_true')

    return parser.parse_args()

def main():
    global exiting
    global sp

    args = parse_args()

    cache_path = os.path.expanduser('~/.config/spockify/token')

    if not os.path.exists(os.path.dirname(cache_path)):
        os.makedirs(os.path.dirname(cache_path))

    scopes = [
        'user-read-playback-state',
        'playlist-read-collaborative',
        'user-modify-playback-state',
    ]

    oauth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri=args.redirect_uri,
        scope=' '.join(scopes),
        cache_path=cache_path,
    )

    token_info = oauth_manager.get_cached_token()

    if not token_info:
        authorization_url = oauth_manager.get_authorize_url()

        print(f'Open {authorization_url} in a browser.')

        code = oauth_manager.parse_response_code(input('Enter the response URL: '))
        token_info = oauth_manager.get_access_token(code)

        with open(cache_path, 'w') as f:
            json.dump(token_info, f)

    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
        client_id=args.client_id,
        client_secret=args.client_secret,
    )

    # credential manager will automatically renew tokens, but doesn't seem to
    # be built to request fully authorized tokens, so this is a hack to force
    # it to support the user authenticated token types.
    client_credentials_manager.token_info = token_info

    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager,
    )

    process_queue_thread = threading.Thread(target=process_queue)
    process_queue_thread.start()

    if args.debug:
        CORS(app, resources=r'/api/.*', allow_headers='Content-Type')
    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        exiting = True

    process_queue_thread.join(timeout=10)

    return True

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
