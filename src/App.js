import React, { Component } from 'react';
import logo from './img/cat.png';
import PropTypes from 'prop-types';

import NowPlaying from './components/NowPlaying.js'
import PlayQueue from './components/PlayQueue.js'
// import './App.css';
import './css/bootstrap.css';
import './css/bootstrap-grid.css';
import './css/app.css';

// spotify:track:0ROCe58wXm7sBUPkZaRrnY
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {errors: [], now_playing: null, queue: null, inputValue: 'spotify:track:0ROCe58wXm7sBUPkZaRrnY'};
  }
  componentDidMount() {
    this.state = {now_playing: null, queue: null};
    fetch("http://127.0.0.1:5000/api/")
    .then(res => {return res.json()})
    .then( res => {
      console.log(res);
      this.setState({now_playing: res.now_playing, queue: res.queue});
    });
  }

  queueSong(e) {
    e.preventDefault();
    fetch('http://127.0.0.1:5000/api/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({spotify_uri: this.state.inputValue})
    })
    .then(res => {return res.json()})
    .then( res => {
      this.setState({queue: res.queue})
    });
  }

  handleInputChange (event) {
    this.setState({inputValue: event.target.value});
  }

  deleteTrack (song, index) {
    console.log(song);
    console.log(index);
  }

  render() {
    return (
      <div className="container-fluid h-100">
        <div className="row mt-5">
            <div className="col-4 offset-4 col-md-2 offset-md-5">
                <img src={logo} className="img-fluid" />
            </div>
        </div>
        
        <NowPlaying now_playing={this.state.now_playing} />

    <div className="row mt-5 mb-5 align-items-center">
      <div className="col-sm-12 col-md-8 offset-md-2">
        <div className="table-responsive">
          <PlayQueue queue={this.state.queue} deleteTrack={this.deleteTrack}/>
          <div className="input-group">
              <input name="spotify_uri"
                     type="text"
                     className="form-control"
                     placeholder="Spotify URI, or URL (tracks or playlists)" 
                     value={this.state.inputValue} onChange={(event) => { this.handleInputChange(event); }}/>
              <div className="input-group-append">
                  <button className="btn btn-success" onClick={(event) => { this.queueSong(event); }}>
                      Queue
                  </button>
              </div>
          </div>
          {
            this.state.errors.length > 0 
            ? (
              <span className="invalid-feedback d-block">
                  Errors : {this.state.errors.map(error => {
                    return error;
                  })}
              </span>
              )
            :
            null
          }
          
        </div>
      </div>
    </div>
    </div>
    );
  }
}

export default App;
