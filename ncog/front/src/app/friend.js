var friend = (function () {

  var tips = {
    80: [
      'This person is on you like white on rice! .',
      'Great job with mirroring their speech patterns.',
      'You clearly listen to this person very well.',
      
      'Good times ahead.',
      'Well done!!'],
    60: [
      "You're doing a pretty good job listening",
      'This person is a friend, but they could be closer ',
      'Going good. Keep up the momentum.',
      'Honey badger! ',
      'Keep it up.'],
    40: [
      'If this is someone you care about, show them. Listen.',
      "Eh. They like you but they wouldn't take a bullet",
      'Consider meeting one on one to build common ground ',
      'Room to grow the relationship',
      'You guys could be greatf riends. '],
    20: [
      'Woa there, they barely know you exist',
      'Try playing hard to get',
      "They're On the fence?",
      'Luke warm reception?',
      'try to connec with them on personal things more.'],
    0: [
      'Never gonna happen, sorry',
      "They think you're weird",
      "Watch out for the restraining order you're sure to get if you keep this up",
      'They respond to about one out of every hundred of your messages. Maybe.',
      'Not working out here.']
  };

function render (friend) {
  
  console.log(friend);
  
  var message;

  if (friend.score < 20) {
    message = tips[0][Math.floor(Math.random()*5)]
  }

  if (friend.score >= 20 && friend.score < 40) {
    message = tips[20][Math.floor(Math.random()*5)]
  }

  if (friend.score >= 40 && friend.score < 60) {
    message = tips[40][Math.floor(Math.random()*5)]
  }

  if (friend.score >= 60 && friend.score < 80) {
    message = tips[60][Math.floor(Math.random()*5)]
  }

  if (friend.score >= 80) {
    message = tips[80][Math.floor(Math.random()*5)]
  }

  var html = '<h1>' + friend.name + '</h1>' +
    '<img src="' + friend.picture + '" />' +
    '<p class="bubble">' + message + '</p>';
    '<h2>Score: ' + friend.score + '</h2>';
  
  $('#friendInfo').html(html);

};

  return {render: render};

}());
