var friendList = (function () {

  var friendsList, pollFriends, totalCalls = 0;

  function init () {

    $('.friendList').on('click', 'li', function(){

     var friend = getByID($(this).attr('data-id'));
    
      renderFriend(friend);

      slider.next();
    });

    fetch();

    pollFriends = setInterval(fetch, 1000);
  }

  function fetch () {

    $.ajax({
        url: '/getFriends',
        type: 'GET',
        success: function(data){ 
          alert('success!');

          console.log(JSON.parse(data));

          friendsList = JSON.parse(data);
          
          render();

          clearInterval(pollFriends);
        },
        error: function(data) {

          totalCalls++;
          
          if (totalCalls > 5) {
            friendsList = fakeFriends;
            clearInterval(pollFriends);
            render();            
          }

        }
    });
  }

  function render () {

    var html = '';

    for (var i in friendsList) {

      var friend = friendsList[i],
          template = 
          '<li data-id="' + friend.id + '">' +
            '<img src="' + friend.picture + '"/>' +
            '<span class="name">' + friend.name + '</span>' + 
            '<span class="score_wrapper"><span class="score" style="background: rgba(0,207,10,' + friend.score/100 + ')">' + friend.score + '</span></span>' + 
          '</li>';

      html += template;
    }

    $('.friendList')
      .html(html)
      .addClass('finished');
  }

  function getByID (id) {

    for (var i in friendsList) {
      if (friendsList[i].id == id) {return friendsList[i]}
    }
    return false
  }

  return {init: init}

}());