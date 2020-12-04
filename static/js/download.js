
$(document).ready(function(){
   
    $('.download-btn').click(function(e){
        e.preventDefault();
      var url =  $(this).attr('src');
      var name =    $(this).data('name');
      var img =   $(this).data('img');
      var artist =   $(this).data('artist');
      var arr = {
          "url":url,
          "name":name,
          "image":img,
          "artist":artist
      }
      alert(arr.image)
    })
})