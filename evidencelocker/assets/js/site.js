// enable/disable signature fields based on perjury oath being selected
$("#oathcheck").change(function(){
  $('.signature-field').prop('disabled', !$('#oathcheck').prop('checked'));
  $('#sig-section').toggleClass('text-muted');
  var txt ='Save';
  if ($('#oathcheck').prop('checked')){
    txt='Sign and Save'
  }
  $('#savebutton').prop('value', txt)
});


//post utility function
function post(url, callback, errortext) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  var form = new FormData()
  form.append("csrf_token", csrftoken());
  xhr.withCredentials=true;
  xhr.onerror=function() { alert(errortext); };
  xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
      callback();
    } else {
      xhr.onerror();
    }
  };
  xhr.send(form);
}

//post form toast utility function
function post_form_toast(form_id, successtext, errortext) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", $('#'+form_id).prop('action'), true);
  var form = new FormData(document.querySelector('#'+form_id))
  xhr.withCredentials=true;
  xhr.onerror=function() { 
      $('#toast-error .toast-text').text(error);
      $('#toast-error').toast()
  };
  xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
      $('#toast-success .toast-text').text(successtext);
      $('#toast-success').toast()
    } else {
      $('#toast-error .toast-text').text(error);
      $('#toast-error').toast()
    }
  };
  xhr.send(form);
}

//Dark mode toggle
$("#dark-mode-toggle").click(function(){
  post('/toggle_darkmode',
    callback=function(){
      var s = $('#mainstyle')
      if( s.prop('href').endsWith('light.css')){
        s.prop('href','/assets/style/dark.css')
      }
      else{
        s.prop('href','/assets/style/light.css')
      }
    })
})
