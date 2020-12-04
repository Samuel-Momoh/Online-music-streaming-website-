// intialize wave
var wave = new Wave()
var options = {type:"wave"}
// Fetch data from database
var songid=  $('#song').val();
var dataString = 'value='+songid

$.ajax({
  url:'/sation',
  type:'POST',
  data: dataString,
  dataType:'JSON',
  cache:false,
  success: function (result){
    $.each(result, function(i, field){
         // fecth lyrics
        //  alert(field[9])
if(field[9]!=null){
  // var newText2 = field[9].replaceAll('[',"\\n[")
  var lrc = new Lyricer({"showLines": 10, "clickable": true});
  lrc.setLrc(field[9]);
  window.addEventListener("lyricerclick", function(e){
    Amplitude.getAudio().currentTime = e.detail.time;
  });
}  
      Amplitude.init({
        "bindings": {
          37: 'prev',
          39: 'next',
          32: 'play_pause'
        },
        debug: true,
  visualization: 'michaelbromley_visualization',
        "songs": [
          {
            "name": field[2],
            "artist": field[1],
            "album": "We Are to Answer",
            "url": '/static/songs/'+field[3],
            "cover_art_url": "/static/album-art/"+field[8],
            "lyrics":field[9],
            "visualization": "michaelbromley_visualization"
          }
        ],
        callbacks:{
          initialized: function(){
          
            var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            fvc.appendChild(audioTag)
            // Pass an Id to Amplitude js audio player
            // Note it very important you add the [0] to the query else it wounldnt work
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
          },
          play: function(){
            var audioTag = Amplitude.getAudio()
            var fvc = document.getElementById('audio')
            $('#audio').empty('')
            fvc.appendChild(audioTag)
            // Pass an Id to Amplitude js audio player
            // Note it very important you add the [0] to the query else it wounldnt work
            document.getElementsByTagName('audio')[0].id="myAudio"
             wave.fromElement("myAudio", "mainCanvas",options)
           document.getElementById("myAudio").currentTime=1
            // lyrics
            var newLyric = Amplitude.getActiveSongMetadata().lyrics
            if(newLyric!=null){
              Amplitude.getAudio().addEventListener( "timeupdate", function() {
                lrc.move(Amplitude.getAudio().currentTime);
              });
            }

            if ('mediaSession' in navigator) {
              navigator.mediaSession.metadata = new MediaMetadata({
                title: Amplitude.getActiveSongMetadata().name,
                artist: Amplitude.getActiveSongMetadata().artist,
                album:"Upring",
                artwork: [
                  { src: 'http://127.0.0.1:5000'+Amplitude.getActiveSongMetadata().cover_art_url,   sizes: '96x96',   type: 'image/png' },
                  { src: 'http://127.0.0.1:5000'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '128x128', type: 'image/png' },
                  { src: 'http://127.0.0.1:5000'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '192x192', type: 'image/png' },
                  { src: 'http://127.0.0.1:5000'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '256x256', type: 'image/png' },
                  { src: 'http://127.0.0.1:5000'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '384x384', type: 'image/png' },
                  { src: 'http://127.0.0.1:5000'+Amplitude.getActiveSongMetadata().cover_art_url, sizes: '512x512', type: 'image/png' },
                ]
              });
            
              navigator.mediaSession.setActionHandler('play', function() {
                Amplitude.play()
              });
              navigator.mediaSession.setActionHandler('pause', function() {
                Amplitude.pause()
              });
              navigator.mediaSession.setActionHandler('seekbackward', function() {
                Amplitude.getAudio().currentTime = Amplitude.getAudio().currentTime - 10
              });
              navigator.mediaSession.setActionHandler('seekforward', function() {
                Amplitude.getAudio().currentTime = Amplitude.getAudio().currentTime +10
              });
              navigator.mediaSession.setActionHandler('previoustrack', function() {
                Amplitude.next( playlistKey = null )
              });
              navigator.mediaSession.setActionHandler('nexttrack', function() { 
                Amplitude.prev( playlistKey = null )
              });
            } 
          },
          pause:function(){
            // wave.pause()
            // alert('i am pause')
          }
          
        }
      });
      // alert(field[8])
      var lyricImage = "/static/album-art/"+field[8]
      $('#lyricer').css('background-image',"url("+lyricImage+")")

      
      });
 
  }
})


  window.onkeydown = function(e) {
      return !(e.keyCode == 32);
  };

  /*
    Handles a click on the song played progress bar.
  */
  document.getElementById('song-played-progress').addEventListener('click', function( e ){
    var offset = this.getBoundingClientRect();
    var x = e.pageX - offset.left;

    Amplitude.setSongPlayedPercentage( ( parseFloat( x ) / parseFloat( this.offsetWidth) ) * 100 );
  });
  // $(document).ready(function(){
  //   alert(Amplitude.getActiveSongMetadata().artist)
       
  // })
           