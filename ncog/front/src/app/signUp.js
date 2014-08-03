function signUp () {

  console.log('here');

  // Sign up submit
  $('#signUp .submit').click(function(){

    setPreference();

    friendList.init();

    slider.next();
  });

  function setPreference () {
    
    var preference = {
      gender: $('select[name="gender"]').val(),
      orientation: $('select[name="orientation"]').val()
    }

    console.log(preference);

    $.ajax({
      type: "POST",
      url: '/lookingFor',
      data: JSON.stringify(preference),
      success: function(){},
      contentType : 'application/json',
      dataType: 'json'
    });
  };

};