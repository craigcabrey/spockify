import React, { Component } from 'react';

class PlayQueue extends Component {
	constructor(props) {
		super(props)
		console.log(this.props)
	}
	openTrackLink = function(track, event) {
		var win = window.open(track.external_urls.spotify, '_blank');
		win.focus();
	}
	render() {
		return (
		<table className="table table-dark table-hover table-borderless">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Title</th>
              <th scope="col">Artist</th>
              <th scope="col">Duration</th>
            </tr>
          </thead>
          <tbody>
          { this.props.queue
          ?
          this.props.queue.map(( item, index ) => {
	          let track = item[0];	
	          return (
	            <tr key={index} className="table-row">
	                <th scope="row">{index}</th>
	                <td onClick={(event, track) =>{this.openTrackLink(track)}}>{track.name}</td>
	                <td>{track.artist}</td>
	                <td>{track.duration}</td>
	                <td onClick={this.props.deleteTrack.bind(this, track, index)} > Delete </td>
	            </tr>
	          );
	        })
            :
            (<tr>
                <th colSpan="4">Nothing in the queue </th>
            </tr>)}
          </tbody>
        </table>);
	}
}

export default PlayQueue;