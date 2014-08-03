var slider = (function () {
  
  var index = 0, slides, nextButtons, previousButtons;
                
  function init () {

    slides = document.querySelectorAll('body > div'),

    nextButtons = document.querySelectorAll('.button.next'),
    previousButtons = document.querySelectorAll('.button.back');

    // Set the position of the gallery to the first slide
    setPosition(index);

    // Bind listeners for gallery controls    
    for (var i in nextButtons) {
      nextButtons[i].onclick = next
    }

    for (var i in previousButtons) {
      previousButtons[i].onclick = previous
    }
  }

  function setPosition (val) {

    var totalSlides = slides.length - 1;
    
    // Ensure position is within the slides
    if (val < 0) {index = val = 0;} 
    if (val > totalSlides) {index = val = totalSlides;} 

    for (var i in slides) {
      
      var slide = slides[i];

      if (i < val) {
        slide.className = 'previous';
      }

      else if (i == val) {
        slide.className = 'current';
      } 

      else if (i > val) {
        slide.className = 'next';
      }
    };
  };

  function next (e) {
    setPosition(++index);
  };

  function previous (e) {
    setPosition(--index);
  };

  return {init: init, next: next, previous: previous}
}());