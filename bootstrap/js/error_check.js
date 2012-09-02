function getErrors() {
  $.get('error', function(data) {
    // Now that we've completed the request schedule the next one.
    if(data != "")
    {
    	$('#error_display').html(data);
    	$('#error_container').fadeIn();
    }
    setTimeout(getErrors, 5000);
  });
}

getErrors();