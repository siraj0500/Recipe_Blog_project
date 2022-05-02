function airTableResetPassword() {
  console.log('POSTing registration reset');
  $.post('https://mrrmrr.herokuapp.com/resetPasswordFed360', ('result=' + JSON.stringify({
      'username': $('#username-input').val(),
      'password': $('#registration-input').val(),
      'newpassword': $('#new-registration-input').val(),
      'email': getEmailParameter()
    })),
    function(data, status) {
      console.log('Data: ' + data + '\nStatus: ' + status);
      if (status !== 'success') {
        alert('error: ' + status);
        return;
      }

      alert('Password has been reset');
      $('#username-input').val('');
      $('#registration-input').val('');
      $('#new-registration-input').val('');
      $('#registration-verification-input').val('');

    }, 'text');

}

function getEmailParameter() {
  var parameters = {};
  // also sets the project name
  var url = window.location.href;
  console.log(url);
  var parametersString = url.split('?')[1];
  if (typeof parametersString == 'undefined') {
    console.log('no url parameter');
    return;
  }
  var parameterString = parametersString.split('&');
  for (var index in parameterString) {
    var keyValue = parameterString[index].split('=');
    var key = keyValue[0];
    var value = decodeURIComponent(keyValue[1]);
    console.log('Webpage URL parameter key,value: ' + key + ',' + value);
    parameters[key] = value;
  }

  if (typeof parameters.email != 'undefined') {
    if (parameters.email.indexOf('#') !== -1) {
      //parameters.email.splice(parameters.email.indexOf('#'), 1);
      //parameters.email.replace9('#','');
      parameters.email = parameters.email.slice(0, -1);
    }
    return parameters.email;
  }

}