$(document).ready(function(){/*
  $(":input").click(function(){
    var espacio_id = $(this).val();
    var form = $(this).closest("form");
    console.log(form.attr("espacio-url"))
    $.ajax({
      url: form.attr("espacio-url"),
      data: {
          'espacio_id': espacio_id
      },
      dataType: 'json',
      success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
      },
      error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
  });*/
});
