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
      url: "/scenarios/scenario/", // same path from action
      data: $(this).serialize(),
      success: function() { // when success response
        //alert('success');
        $("#load").hide();
        window.location.href = "/scenarios/results/";
      },
      error: function(){
        alert('Ocorreu um erro! Retornando para a página principal!');
        window.location.href = "/";
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


    $('#loadscenario').on('submit', function(e) { // form when submit action
      //console.log($(this).serialize()); // log for see the form data serialzed which is equal to the one send when submit normally
      e.preventDefault(); //prevet default action
      $.ajax({ // http call
        type: "POST", // method
        url: "/scenarios/", // same path from action
        data: $(this).serialize(),
        success: function() { // when success response
          window.location.href = "/scenarios/scenario/";
        },
        error: function(erro){
          console.log(erro)
          alert('Erro em identificar as ferramentas no HOST Remoto! Retornando para a página principal.');
	  //Talvez seja interessante realizar o log desse erro aqui! Para facilitar a identificação posterior!
          window.location.href = "/";

      }
      });
      return false;
    });












});
