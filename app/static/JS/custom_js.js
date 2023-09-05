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
    var imageWidth = $('#responsive-image').width();
    var imageHeight = $('#responsive-image').height();

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
  var originalImageWidth = $('#responsive-image').width();
  
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

