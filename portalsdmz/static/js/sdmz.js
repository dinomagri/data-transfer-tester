// $(document).ready(function($) {
//   $('#meuForm').on('submit', function(e) { // form when submit action
//     console.log($(this).serialize()); // log for see the form data serialzed which is equal to the one send when submit normally
//     e.preventDefault(); //prevet default action
//     $.ajax({ // http call
//       type: "POST", // method
//       url: "/scenarios/", // same path from action
//       data: $(this).serialize(),
//       success: function() { // when success response
//         alert('success');
//       }
//     });
//     return false;
//   });
// });
$(document).ready(function($) {
  $('#loadform').on('submit', function(e) { // form when submit action
    //console.log($(this).serialize()); // log for see the form data serialzed which is equal to the one send when submit normally
    e.preventDefault(); //prevet default action
    $("#load").show();
    $.ajax({ // http call
      type: "POST", // method
      url: "/scenarios/", // same path from action
      data: $(this).serialize(),
      success: function() { // when success response
        //alert('success');
        $("#load").hide();
        window.location.href = "/scenarios/results/";
      },
      error: function(){
        alert('algum erro ocorreu!');
        window.location.href = "/scenarios/";
    }
    });
    return false;
  });
  $("#id_wget").change(function() {
    if (this.checked) {
      $("#id_fluxo").hide();
    } else {
      $("#id_fluxo").show();
    }
  })
  $("#id_scp").change(function() {
    if (this.checked) {
      $("#id_fluxo").hide();
    } else {
      $("#id_fluxo").show();
    }
  })
});



$(document).ready(function($) {
  $('#loadscenario').on('submit', function(e) { // form when submit action
    //console.log($(this).serialize()); // log for see the form data serialzed which is equal to the one send when submit normally
    e.preventDefault(); //prevet default action
    $.ajax({ // http call
      type: "POST", // method
      url: "/", // same path from action
      data: $(this).serialize(),
      success: function() { // when success response
        window.location.href = "/scenarios";
      },
      error: function(){
        alert('algum erro ocorreu!, mas foi o botao certo');
        window.location.href = "/";
    }
    });
    return false;
  });
});
