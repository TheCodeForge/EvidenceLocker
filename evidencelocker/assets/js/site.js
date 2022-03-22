// enable/disable signature fields based on perjury oath being selected
$("#oathcheck").change(function(){
  $('.signature-field').prop('disabled', !$('#oathcheck').prop('checked'));
  $('#sig-section').toggleClass('text-muted')
  var txt ='Save'
  if ($('#oathcheck').prop('checked')){
    txt='Sign and Save'
  }
  $('#savebutton').prop('value', txt)
});

