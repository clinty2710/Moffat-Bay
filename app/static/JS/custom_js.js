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

  // Define your mapster configuration
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
    showToolTip: true,
    onClick: function (e) {
      var roomNumber = e.key.replace("room_", "");
      $('#room_number').val(roomNumber);
      console.log(roomNumber);
    },
    toolTipClose: ["tooltip-click", "area-click"],
    areas: [
      // rooms 1_
      {
        key: "room_1a",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1b",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1c",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1d",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1e",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1f",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1g",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_1h",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      // rooms 2_
      {
        key: "room_2a",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2b",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2c",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2d",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2e",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2f",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2g",
        fillColor: "c0d904",
        strokeColor: "055902"
      },
      {
        key: "room_2h",
        fillColor: "c0d904",
        strokeColor: "055902"
      }
    ]
  });

  $('#room_number').on('change', function () {
    var selectedRoom = $(this).val();

    // Deselect all areas first
    image.mapster('deselect');

    // Select the area corresponding to the selected room
    image.mapster('set', true, 'room_' + selectedRoom);
  });

  $('#start_date, #end_date').on('change', function () {
    // Get the selected start and end dates
    var startDate = $('#start_date').val();
    var endDate = $('#end_date').val();

    // Make an AJAX request to the Flask route to get room availability
    $.ajax({
      url: '/get_room_availability',
      type: 'GET',
      data: { start_date: startDate, end_date: endDate },
      success: function (response) {
        var unavailableRooms = response;

        // Update the image map to mark unavailable rooms
        updateImageMap(unavailableRooms);
      },
      error: function (error) {
        console.error(error);
      }
    });
  });

  function updateImageMap(unavailableRooms) {
    for (var i = 0; i < unavailableRooms.length; i++) {
      unavailableRooms[i] = 'room_' + unavailableRooms[i];
      image.mapster('set', true, unavailableRooms[i]);
      console.log(unavailableRooms[i]);
    }
  }
});


