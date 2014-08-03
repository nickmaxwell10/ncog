var fakeNames = [
  'Christen Fandel',
  'Twyla Ronald',
  'Sheri Carmona',
  'Joleen Hausner',
  'Margret Deibert',
  'Harriet Hiler',
  'Miguel Borgeson',
  'Jamar Nipper',
  'Elias Stufflebeam',
  'Keira Duenas',
  'Leora Motz',
  'Fabian Gatson',
  'Vilma Mcafee',
  'Christine Garand',
  'Allegra Ivers',
  'Brenda Irwin',
  'Tatyana Vandergriff',
  'Tangela Jenny',
  'Darleen Gregory',
  'Eloy Vanduyne'
], fakeFriends = (function makeFakeFriends () {

  var list = {},
       max = 100;

  for (var i in fakeNames) {
    max -= Math.round(Math.random()*10);
    if (max < 0) max = 0;
    list[i] = {
      name: fakeNames[i],
      id: [i],
      picture: 'images/samples/' + i + '.jpg',
      score: max
    }
  }

  return list
}());
