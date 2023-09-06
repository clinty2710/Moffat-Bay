/*  Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
    CSD460 Capstone Project
    custom_js.js
*/

// Fade out the flash messages after 5 seconds
setTimeout(function() {
    $('#flash-messages').fadeOut('slow');
}, 5000);  // 5000 milliseconds = 5 seconds
$(document).ready(function() {
  // Function to update area coordinates based on the current image size
  function updateAreaCoordinates() {
    var imageWidth = $('#hotel-image').width();
    var imageHeight = $('#hotel-image').height();

    // Calculate new coordinates for each area
    $('map[name="image-map"] area').each(function() {
      var originalCoords = $(this).data('original-coords').split(',');
      var scaledCoords = originalCoords.map(function(coord) {
        return coord * (imageWidth / originalImageWidth);
      });
      $(this).attr('coords', scaledCoords.join(','));
    });
  }

  // Save original image dimensions
  var originalImageWidth = $('#hotel-image').width();
  
  // Store original coordinates as data attribute for each area
  $('map[name="image-map"] area').each(function() {
    var originalCoords = $(this).attr('coords');
    $(this).data('original-coords', originalCoords);
  });

  // Update coordinates on window resize
  $(window).resize(function() {
    updateAreaCoordinates();
  });

  // Initial update
  updateAreaCoordinates();
});
var xref = {
  room_1a: "<b>Carrots</b> are delicious and may turn your skin orange!",
  room_1b: "<b>Asparagus</b> is one of the first vegetables of the spring. " 
      +"Being a dark green, it's great for you, and has interesting side effects.",
  room_1c: "<b>Squash</b> is a winter vegetable, and not eaten raw too much. Is that really squash?",
  room_1d: "<b>Red peppers</b> are actually the same as green peppers, they've just been left on "
      +"the vine longer. Delicious when fire-roasted.",
  room_1e: "Similar to red peppers, <b>yellow peppers</b> are sometimes sweeter.",
  room_1f: "<b>Celery</b> is a fascinating vegetable. Being mostly water, it actually takes your body "
      +"more calories to process it than it provides.",
  room_1g: "<b>Cucumbers</b> are cool.",
  room_1h: "<b>Broccoli</b> is like a forest of goodness in your mouth. And very good for you. "
  +"Eat lots of broccoli!",
  room_2a: "<b>Carrots</b> are delicious and may turn your skin orange!",
  room_2b: "<b>Asparagus</b> is one of the first vegetables of the spring. " 
  +"Being a dark green, it's great for you, and has interesting side effects.",
  room_2c: "<b>Squash</b> is a winter vegetable, and not eaten raw too much. Is that really squash?",
  room_2d: "<b>Red peppers</b> are actually the same as green peppers, they've just been left on "
  +"the vine longer. Delicious when fire-roasted.",
  room_2e: "Similar to red peppers, <b>yellow peppers</b> are sometimes sweeter.",
  room_2f: "<b>Celery</b> is a fascinating vegetable. Being mostly water, it actually takes your body "
  +"more calories to process it than it provides.",
  room_2g: "<b>Cucumbers</b> are cool.",
  room_2h: "<b>Broccoli</b> is like a forest of goodness in your mouth. And very good for you. "
  +"Eat lots of broccoli!",
};
$(document).ready(function() {
  var image = $('#hotel-image');
  image.mapster(
    {
        fillOpacity: 0.4,
        fillColor: "d42e16",
        stroke: true,
        strokeColor: "3320FF",
        strokeOpacity: 0.8,
        strokeWidth: 4,
        singleSelect: true,
        mapKey: 'name',
        listKey: 'name',
        onClick: function (e) {
            // update text depending on area selected
            $('#selections').html(xref[e.key]);
  
        },
        showToolTip: true,
        toolTipClose: ["tooltip-click", "area-click"],
        areas: [
            {
                key: "room_1a",
                fillColor: "ffffff"
            },
            {
                key: "room_1b",
                fillColor: "000000"
            },
            {
                key: "room_1c",
                fillColor: "000000"
            },
            {
                key: "room_1d",
                fillColor: "000000"
            },
            {
                key: "room_1e",
                strokeColor: "FFFFFF"
            }
            ]
    });
  
});
