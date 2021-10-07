'use strict';

$(document).ready(function() {
    var progressContainer = document.getElementById('progress-container');
    var searchText = $("#video-search input:text"); 

    // markers
    function addMarker(video, second) {
        var marker = $("<div class='marker'></div>");
        var offset = Math.floor((second / video.duration) * 100) + '%';
        marker.css("margin-left", offset);
        $(progressContainer).prepend(marker);
        marker.click(function() {
            video.currentTime = second;
        });
    }
    function clearMarkers() {
        $(".marker").remove();
    }

    // search video
    searchText.keyup(function() {
        clearMarkers();
        var string = $(this).val();
        var markers = [];
        if (string) {
            for (var i=0; i<liquid.length; i++) {
                var el = liquid[i];
                if (el.join(' ').includes(string)) {
                    markers.push(i);
                }
            }
            markers.forEach(i => addMarker(video, i));
        }
    });
});
