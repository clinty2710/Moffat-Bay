/*  Charlie Team: Clint Steadman, joshua Welch, Aura Elle Winters, Riese Bohnak
    CSD460 Capstone Project
    custom_js.js
*/

// Fade out the flash messages after 5 seconds
setTimeout(function () {
  $('#flash-messages').fadeOut('slow');
}, 5000);  // 5000 milliseconds = 5 seconds
$(document).ready(function () {
  // Function to update area coordinates based on the current image size
  function updateAreaCoordinates() {
    var imageWidth = $('#hotel-image').width();
    var imageHeight = $('#hotel-image').height();

    // Calculate new coordinates for each area
    $('map[name="image-map"] area').each(function () {
      var originalCoords = $(this).data('original-coords').split(',');
      var scaledCoords = originalCoords.map(function (coord) {
        return coord * (imageWidth / originalImageWidth);
      });
      $(this).attr('coords', scaledCoords.join(','));
    });
  }

  // Save original image dimensions
  var originalImageWidth = $('#hotel-image').width();

  // Store original coordinates as data attribute for each area
  $('map[name="image-map"] area').each(function () {
    var originalCoords = $(this).attr('coords');
    $(this).data('original-coords', originalCoords);
  });

  // Update coordinates on window resize
  $(window).resize(function () {
    updateAreaCoordinates();
  });

  // Initial update
  updateAreaCoordinates();
});
$(document).ready(function () {
  var image = $('#hotel-image');
  image.mapster({
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
      
      var roomNumber = e.key.replace("room_", "");
      $('#room_number').val(roomNumber);
      console.log(roomNumber);
    },
    showToolTip: true,
    toolTipClose: ["tooltip-click", "area-click"],
    areas: [
      {
        key: "room_1a",
        fillColor: "000000"
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
        strokeColor: "000000"
      }
    ]
  });

});
