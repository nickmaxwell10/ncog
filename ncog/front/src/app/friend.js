var friend = (function () {

  var tips = {
    80: [
      'Working it.',
      'All around goodness is happening.',
      'On fire!',
      'Good times ahead.',
      'Getting hot in here!'],
    60: [
      'Making a positive impression.',
      'Beyond flirting. ',
      'Going good. Keep the momentum.',
      'Honey badger! ',
      'Keep it up.'],
    40: [
      'Keep it up to warm up.',
      'Are they floating your boat?',
      'Are they digging you? ',
      'Something more developing?',
      'Have you meet up yet? '],
    20: [
      'Not as interested?',
      'Text slow down?',
      'On the fence?',
      'Luke warm reception?',
      'Need to warm up more?'],
    0: [
      'Not sure they are as into you.',
      'Not that into them?',
      'Dropping it like it’s hot?',
      'Too busy to text?',
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
