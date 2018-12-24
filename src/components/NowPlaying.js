import React, { Component } from 'react';

class NowPlaying extends Component {
	render () { 
		if (this.props.now_playing) {
			return (
				<div className="row mt-5 align-items-center">
	            <div className="col-1 offset-md-2">
	              <img className="rounded img-thumbnail image-fluid float-left" 
	              		src={this.props.now_playing.album_art_url} />
	            </div>
	              <div className="col-9">
	                  <h3>{this.props.now_playing.item.name}</h3>
	                  <small className="text-muted">{this.props.now_playing.artist}</small>
	              </div>
	        	</div>
	        ) 
		} else {
			return null;
		}
	}
}

export default NowPlaying;
