
// Trending link copy
    var trending=new ClipboardJS('.share');
    trending.on('success',function(e){e.clearSelection();
        console.info('Trigger:',e.trigger);
        showTooltip(e.trigger,'Copied!');});
        trending.on('error',function(e){console.error('Action:',e.action);console.error('Trigger:',e.trigger);showTooltip(e.trigger,fallbackMessage(e.action));});

        var trending_btn=document.querySelectorAll('.share');for(var i=0;i<trending_btn.length;i++){trending_btn[i].addEventListener('mouseleave',clearTooltip);trending_btn[i].addEventListener('blur',clearTooltip);}
        function clearTooltip(e){e.currentTarget.classList.remove('visible');}
        function showTooltip(elem){elem.classList.add('visible');}
        function fallbackMessage(action){var actionMsg='';var actionKey=(action==='cut'?'X':'C');if(/iPhone|iPad/i.test(navigator.userAgent)){actionMsg='No support :(';}
        else if(/Mac/i.test(navigator.userAgent)){actionMsg='Press ⌘-'+actionKey+' to '+action;}
        else{actionMsg='Press Ctrl-'+actionKey+' to '+action;}
        return actionMsg;}


// Search modal
          // Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
// When the user clicks on the button, open the modal
// btn.onclick = function() {
//   modal.style.display = "block";
// }

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
  $('.empty').css('display','none')
  $('.search-content').remove()
  $('.modal-content a').remove()
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    $('.empty').css('display','none')
    $('.search-content').remove()
    $('.modal-content a').remove()
  }
} 

// Search Query
$(document).ready(function(){
  $('#myBtn').click(function(){
    
    $('.modal-content').css('display','none');
    $('#loader-wrapper').css('display','block')
   var searchItem = $('#searchItem').val();
    if(searchItem==''){
      $('#searchItem').css('border-color','red');
    }else{
  $('#searchItem').css('border-color','#f7f7f7');
// Checking if text contains @
if(searchItem.includes("@")){
  var newitem = searchItem.replace('@','')
  var dataString = 'value='+newitem
  $.ajax({
    url:'/searchartist',
    type:'POST',
    data: dataString,
    dataType:'JSON',
    cache:false,
    success: function (result){
      if(result.length==0){
        modal.style.display = "block";
        $('.empty').css('display','block')
        setTimeout(function(){
  $('#loader-wrapper').css('display','none')
  $('.modal-content').css('display','block');
        },3000)
      }else{
      $.each(result, function(i, field){
        output = '<a href="http://127.0.0.1:5000/artist/'+field[1]+'"> <div class="search-artist">';
      output += '<div class="search-image"><img src="/static/album-art/'+field[3]+'" alt="" > </div>';
      output += '<div class="search-text"> <h1>'+field[1]+'</h1> <p>'+field[2]+'</p><a href="http://127.0.0.1:5000/artist/'+field[1]+'">http://127.0.0.1:5000/artist/'+field[1]+'</a></div>';
      output += '</div></a>';
      $('.search-query').append(output);
      modal.style.display = "block";
      setTimeout(function(){
$('#loader-wrapper').css('display','none')
$('.modal-content').css('display','block');
      },3000)
        });
      }
    

    }
  });

}else{
  var dataString = 'value='+searchItem
  
  $.ajax({
    url:'/searchsong',
    type:'POST',
    data: dataString,
    dataType:'JSON',
    cache:false,
    success: function (result){

      if(result.length==0){
        modal.style.display = "block";
        $('.empty').css('display','block')
        setTimeout(function(){
  $('#loader-wrapper').css('display','none')
  $('.modal-content').css('display','block');
        },3000)
      }else{
        $.each(result, function(i, field){
          output = '<a href="http://127.0.0.1:5000/songs/'+field[0]+'"> <div class="search-content">';
          output += '<div class="search-image"><img src="/static/album-art/'+field[8]+'" alt="" > </div>';
          output += '<div class="search-text"> <h1>'+field[1]+'</h1> <p>'+field[2]+'</p><a href="http://127.0.0.1:5000/songs/'+field[0]+'">http://127.0.0.1:5000/songs/'+field[0]+'</a><p>'+field[6]+'</p></div>';
          output += '</div></a>';
          $('.search-query').append(output);
          modal.style.display = "block";
          setTimeout(function(){
    $('#loader-wrapper').css('display','none')
    $('.modal-content').css('display','block');
          },3000)
          });
      }


    }
  });
}



    }
 
  });
  setTimeout(function(){
$('body').removeClass('body-hide');
$('.preloader-body').css('display','none');
  },5000)
});

// Full screen
/* Get the documentElement (<html>) to display the page in fullscreen */
var elem = document.getElementById('blue-playlist-container');

/* View in fullscreen */
function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) { /* Firefox */
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE/Edge */
    elem.msRequestFullscreen();
  }
}

/* Close fullscreen */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) { /* Firefox */
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE/Edge */
    document.msExitFullscreen();
  }
}