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
        url: '/friends',
        type: 'GET',
        success: function(data){ 

          if (data.status === 'complete') {

            console.log('complete!');

            friendsList = data.friends;

            console.log(data);

            for (var i in friendsList) {
              friendsList[i].score = friendsList[i].score || Math.round(Math.random()*100);
              friendsList[i].picture = 'http://graph.facebook.com/' + friendsList[i].user_id + '/picture?type=large';
            };

            render();

            clearInterval(pollFriends);

          }          
        },
        error: function(data) {

          totalCalls++;
          
          if (totalCalls > 5) {
            friendsList = fakeFriends;
            clearInterval(pollFriends);
            pollFriends = setInterval(fetch, 2000);
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