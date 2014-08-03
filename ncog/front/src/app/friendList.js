var friendList = (function () {

  var friendsList, pollFriends, pollScores, totalCalls = 0;

  function init () {

    $('.friendList').on('click', 'li', function(){

     var friend = getByID($(this).attr('data-id'));
    
      renderFriend(friend);

      slider.next();

      $("html, body").animate({ scrollTop: 0 }, "slow");
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
              friendsList[i].score = friendsList[i].score || ''; 
              friendsList[i].picture = "http://graph.facebook.com/" + friendsList[i].user_id + "/picture?height=200&width=200";
            };

            render();

            clearInterval(pollFriends);

            getScores();

            var pollScores = setInterval(getScores, 1000);

          }          
        },
        error: function(data) {}
    });
  }

  function getScores () {

    $.ajax({
        url: '/scores',
        type: 'GET',
        success: function(data){ 

          if (data.status === 'complete') {

            console.log('complete!');

            for (var i in data.scores) {

              var friendID = data.scores[i].other_id,
                  friendScore = data.scores[i].other_score;

              for (var i in friendsList) {

                if (friendsList[i].id == friendID) {
                    friendsList[i].score = friendScore;
                }
              };
            }

            render();

            clearInterval(pollScores);

          }          
        },
        error: function(data) {}
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