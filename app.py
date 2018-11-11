#!/usr/bin/env python3

import argparse
import sys

import flask
import spotipy
import spotipy.util

app = flask.Flask(__name__)


sp = None


@app.route('/', methods=['GET'])
def get_index():
    return flask.render_template('index.html')

@app.route('/', methods=['POST'])
def post_index():
    uri = flask.request.form.get('spotify_uri')
    sp.start_playback(uris=[uri])
    return flask.redirect('/')

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('username')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000)

    return parser.parse_args()

def main():
    global sp

    args = parse_args()

    token = spotipy.util.prompt_for_user_token(
        args.username,
        'user-modify-playback-state',
    )

    sp = spotipy.Spotify(auth=token)

    app.run(host=args.host, port=args.port)

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
