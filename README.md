# spockify

Simply put, `spockify` is an application that provides a shared queue through Spotify Connect. Anyone with local access to the service can add to and view this shared queue simply by visting the web application (though we can imagine implementing some basic authentication down the road).

## requirements

Written and tested with Python 3.7 (as of this writing of course). No guarantees of anything less than the latest version of Python is a good rule of thumb here.

We also make use of `flask` and `spotipy` to make all the glue coding easier (thanks for that).

## getting started

Register a Spotify application under your account. See Spotify's guide [here](https://developer.spotify.com/documentation/general/guides/authorization-guide/). Note that this may end up being out of date at some point.

You'll need to set the environment variables that `spotipy` uses (or alternatively just use the equivalent command line arguments, see `--help` for more):

* `SPOCKIFY_CLIENT_ID`
* `SPOCKIFY_CLIENT_SECRET`
* `SPOCKIFY_REDIRECT_URI`

The first two are self explanatory (hopefully), and the second can just be set to `http://localhost/` -- though note that you need to authorize this redirect uri in the settings of your registered Spotify application.

Once you have those sorted out and you'll installed all the dependencies, just run `python3 app.py {username}`. Your browser will open asking you to authenticate and authorize with Spotify. When Spotify redirects you, just grab the url from your browser and paste it into the prompt that is waiting. Then, you should be good to go. Visit localhost:5000 in your browser.

This is a super hacked up prototype at this point so don't expect anything fancy.

## screenshot

![screenshot of the spockify ui](https://raw.githubusercontent.com/craigcabrey/spockify/master/static/screenshot.png)

## License

GPLv3, see LICENSE
