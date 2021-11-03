'use strict';

$(document).ready(function() {
    var progressContainer = $("#progress-container");
    var searchText = $("#video-search input:text");

    // markers
    function addMarker(video, second) {
        var marker = $("<div class='marker'></div>");
        var offset = (second / video.duration) * 100 + '%';
        marker.css("margin-left", offset);
        progressContainer.prepend(marker);
        marker.click(function() {
            video.currentTime = second;
        });
    }
    function clearMarkers() {
        $(".marker").remove();
    }

    // add ims
    function addIm(second, im_url) {
        var im = $(`
<div class="thumbnail">
    <div class="thumbnail-overlay" id="thumbnail-${second}">
        <div class="thumbnail-seconds">${renderTime(second, 3054)}</div>
    </div>
    <img src='${im_url}'/>
</div>
`);
        $("#search-images").append(im);
        $("#thumbnail-" + second).click(function() {
            video.currentTime = second;
        });
    }

    function clearIms() {
        $("#search-images").empty();
    }

    // search video
    searchText.keyup(function() {
        clearMarkers();
        clearIms();
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

            // hack
            if (liquid_desc.includes("search")) {
                markers.forEach(i => addIm(i, liquid[i]));
                $("#search-images .thumbnail").hover(function() {
                    $(this).find(".thumbnail-overlay").show();
                }, function() {
                    $(this).find(".thumbnail-overlay").hide();
                });
            }
        }
    });
});
