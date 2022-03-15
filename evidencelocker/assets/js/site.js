// enable/disable signature fields based on perjury oath being selected
$("#oathcheck").change(function(){
  $('#input-password').prop('disabled', !$('#oathcheck').prop('checked'))
});

