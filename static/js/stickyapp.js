var run;
$(document).ready(function()
{
player = $('body').stickyAudioPlayer(
{
url:       'http://localhost/fmuzic/songs/bensound-betterdays.mp3',
position:  'bottom',
text:      'Bensound - Going Higher - Music: http://www.bensound.com',
image:     'http://tiendasdigitales.net/github/stickyaudioplayerjquery/images/cover.png',
volume:    40,
image:     'static/images/cover.png',
repeat:    false,
}
);
// Change songs
$('.playBtn').click(function(e) {
    e.preventDefault(); 
    var src = $(this).attr('href');
    var title = $(this).data("title");
    var img = $(this).data("img");
    var sondtitle = $(this).data("name");
    var sondartist = $(this).data("artist");
    var sondgenre = $(this).data("genre");
    player.changeAudio(src,title,img,sondtitle,sondartist,sondgenre);
});


});

