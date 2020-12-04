// intialize wave
var wave = new Wave()
var options = {type:"wave"}
// Intialize Lyricer js
var lrc = new Lyricer({"showLines": 8, "clickable": true});
/*
	When the bandcamp link is pressed, stop all propagation so AmplitudeJS doesn't
	play the song.
*/
let bandcampLinks = document.getElementsByClassName('bandcamp-link');

for( var i = 0; i < bandcampLinks.length; i++ ){
	bandcampLinks[i].addEventListener('click', function(e){
		e.stopPropagation();
	});
}


let songElements = document.getElementsByClassName('song');

for( var i = 0; i < songElements.length; i++ ){
	/*
		Ensure that on mouseover, CSS styles don't get messed up for active songs.
	*/
	songElements[i].addEventListener('mouseover', function(){
		this.style.backgroundColor = '#242b33';

		if( !this.classList.contains('amplitude-active-song-container') ){
			this.querySelectorAll('.play-button-container')[0].style.display = 'block';
		}
	});

	/*
		Ensure that on mouseout, CSS styles don't get messed up for active songs.
	*/
	songElements[i].addEventListener('mouseout', function(){
		this.style.backgroundColor = '#30363e';
		this.querySelectorAll('.play-button-container')[0].style.display = 'none';
	});

	/*
		Show and hide the play button container on the song when the song is clicked.
	*/
	songElements[i].addEventListener('click', function(){
		// this.style.backgroundColor ='#242b33';
		this.querySelectorAll('.play-button-container')[0].style.display = 'none';
		setTimeout(function(){
			// Wave js
			var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            $('#audio').empty('')
            fvc.appendChild(audioTag)
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
           document.getElementById("myAudio").currentTime=1
			// fetch lyrics
		$('#lyricer').empty('')
		var newLyric = Amplitude.getActiveSongMetadata().lyrics
		// alert(newLyric)
			if(newLyric!=null){
				var newImage = Amplitude.getActiveSongMetadata().cover_art_url
				lrc.setLrc(newLyric);
	$('#lyricer').css('background-image',"url("+newImage+")")
			}else{
				var newImage = Amplitude.getActiveSongMetadata().cover_art_url
				$('#lyricer').css('background-image',"url("+newImage+")")
			}
		},100)
		var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            $('#audio').empty('')
            fvc.appendChild(audioTag)
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
		
	});
}

/*
	Initializes AmplitudeJS
*/
var songid=  $('#song').val();
var json=[]
var dataString = 'value='+songid
$.ajax({
  url:'/sgenre',
  type:'POST',
  data: dataString,
  dataType:'JSON',
  cache:false,
  success: function (data){
// alert(data[0][9])
if(data[0][9]!=null){
	var lyricImage = "/static/album-art/"+data[0][8]
	$('#lyricer').css('background-image',"url("+lyricImage+")")
	//    fecth lyrics
	//    var newText2 = data[0][9].replaceAll('[',"\\n[")
	   var newText2 = data[0][9]
	   lrc.setLrc(newText2);
	   window.addEventListener("lyricerclick", function(e){
		Amplitude.getAudio().currentTime = e.detail.time;
	   });
}else{
	var lyricImage = "/static/album-art/"+data[0][8]
	$('#lyricer').css('background-image',"url("+lyricImage+")")
}

	for(var i in data) {
		var arr={
			"name": data[i][2],
			"artist": data[i][1],
			"album": "We Are to Answer",
			"url": '/static/songs/'+data[i][3],
			"cover_art_url": "/static/album-art/"+data[i][8],
			"lyrics": data[i][9]
		}
		json.push(arr)
	}

Amplitude.init({
	"bindings": {
	  37: 'prev',
	  39: 'next',
	  32: 'play_pause'
	},
	callbacks:{
		initialized: function(){
          
            var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            fvc.appendChild(audioTag)
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
          },
		play: function(){
			var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            fvc.appendChild(audioTag)
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
			// alert('yes')
			var newLyric = Amplitude.getActiveSongMetadata().lyrics
			if(newLyric!=null){
				Amplitude.getAudio().addEventListener( "timeupdate", function() {
					lrc.move(Amplitude.getAudio().currentTime);
				  });
			}
		
		},
		next: function(){
			var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            $('#audio').empty('')
            fvc.appendChild(audioTag)
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
		   document.getElementById("myAudio").currentTime=1
		//    lyricer
			$('#lyricer').empty('')
			var newLyric = Amplitude.getActiveSongMetadata().lyrics
			// alert(newLyric)
			if(newLyric!=null){
				var newImage = Amplitude.getActiveSongMetadata().cover_art_url
				lrc.setLrc(newLyric);
	$('#lyricer').css('background-image',"url("+newImage+")")
			}else{
				var lyricImage = "/static/album-art/"+data[0][8]
				$('#lyricer').css('background-image',"url("+lyricImage+")")
			}
		
		},
		prev: function(){ 
			var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            $('#audio').empty('')
            fvc.appendChild(audioTag)
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
                                 
			$('#lyricer').empty('')
			var newLyric = Amplitude.getActiveSongMetadata().lyrics
			// alert(newLyric)
			if(newLyric!=null){
				var newImage = Amplitude.getActiveSongMetadata().cover_art_url
				lrc.setLrc(newLyric);
	$('#lyricer').css('background-image',"url("+newImage+")")
			}else{
				var lyricImage = "/static/album-art/"+data[0][8]
				$('#lyricer').css('background-image',"url("+lyricImage+")")
			}
		}
	},
	"songs": json
	
	
  });

  }
});
