// <!--<div id="previousRelationships">
//       <div>
//         <h1>Have you been in a relationship with any of your facebook friends?</h1>
//         <div id="previousToggle">
//           <a class="button yes">Yes, I am friends with an ex</a>        
//           <a class="button no next secondary">No, I am not</a>        
//         </div>
//         <div class="yes inset" style="display:none">
//           <hr>
//           <span>What is your ex's name?</span>
//           <input type="text" placeholder="Type your ex's name..." class="large friendSearch typeahead" />
//           <div class="results"></div>
//           <a class="button next">Continue</a>                  
//         </div>
//         <Br /><hr>        
//         <h5 class="lock">This information is not shared with anyone</h5>
//       </div>
//     </div>
//     <div id="futureRelationships">
//       <div>      
//         <h1>Which of your facebook friends are you really close to?</h1>
//         <h2>This information is not shared with anyone</h2>
//         <input type="text" placeholder="Type your friend's name..." class="large friendSearch typeahead" />
//         <div class="results"></div>
//         <a class="button next">Next</a>        
//         <h5 class="lock">This information is not shared with anyone</h5>
//       </div>
//     </div>-->

// function substringMatcher (strs) {
//   return function findMatches(q, cb) {
//     var matches, substrRegex;
 
//     // an array that will be populated with substring matches
//     matches = [];
 
//     // regex used to determine if a string contains the substring `q`
//     substrRegex = new RegExp(q, 'i');
 
//     // iterate through the pool of strings and for any string that
//     // contains the substring `q`, add it to the `matches` array
//     $.each(strs, function(i, str) {
//       if (substrRegex.test(str)) {
//         // the typeahead jQuery plugin expects suggestions to a
//         // JavaScript object, refer to typeahead docs for more info
//         matches.push({ value: str });
//       }
//     });
 
//     cb(matches);
//   };
// };


// $('#previousRelationships .button.yes').click(function(){
  
//   $(this).toggleClass('selected');
//   $('div.yes').toggle();

// });

// // Autocomplete input for friend selection
// var autoCompleteOptions = {
//     hint: true,
//     highlight: true,
//     minLength: 1
//   },
//   friendSearchOptions = {
//     name: 'friends',
//     displayKey: 'value',
//     source: substringMatcher(friends)
//   };

// $('input.friendSearch')
//   .keyup(onKeyUp)
//   .typeahead(autoCompleteOptions, friendSearchOptions);

// $('a.remove').click(function(){
//   $(this).parent().remove();
// });

// function onKeyUp (e) {
//   if (e.keyCode == 13) {
    
//     var html = '<p>' + $(this).val() + '<a href="#" class="remove">X</a></p>';

//     $(this)
//       .val('')
//       .parents('div')
//       .first()
//       .find('.results')
//       .append(html)
//   }
// }

// var friends = {},
//     exes = {},
//     closeFriends = {};