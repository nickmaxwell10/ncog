function renderFriend(friend) {
  
  var html = 
    '<h1>' + friend.name + '</h1>' +
    '<img src="' + friend.picture + '" />' +
    '<h2>Score: ' + friend.score + '</h2>';
  
  $('#friendInfo').html(html);
}