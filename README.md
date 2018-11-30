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

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

## License

GPLv3, see LICENSE
