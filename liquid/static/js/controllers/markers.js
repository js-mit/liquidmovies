"use strict";

$(document).ready(function () {
    var progressContainer = $("#progress-container");
    var searchText = $("#video-search input:text");
    var topwords = $("topwords-container");

    // markers
    function addMarker(video, second) {
        var marker = $("<div class='marker'></div>");
        var offset = (second / video.duration) * 100 + "%";
        marker.css("margin-left", offset);
        progressContainer.prepend(marker);
        marker.click(function () {
            video.currentTime = second;
        });
    }

    function clearMarkers() {
        $(".marker").remove();
    }

    // add ims
    function addIm(index, second, im_url, duration) {
        second = parseInt(second);
        var im = $(`
<div class="thumbnail">
    <div class="thumbnail-overlay" id="thumbnail-${index}-${second}">
        <div class="thumbnail-seconds">${renderTime(second, duration)}</div>
    </div>
    <img src='${im_url}'/>
</div>
`);
        $("#search-images").append(im);
        $("#thumbnail-" + index + "-" + second).click(function () {
            console.log("Click happened.");
            video.currentTime = second;
        });
    }

    function clearIms() {
        $("#search-images").empty();
    }

    function searchimages(string) {
        clearMarkers();
        clearIms();
        var markers = [];
        var frameUrls = [];
        // set up markers
        for (var i = 0; i < _data.length; i++) {
            var el = _data[i];
            var label = el["Label"]["Name"].toLowerCase();
            var confidence = parseFloat(el["Label"]["Confidence"]);
            if (confidence >= 97.5) {
                if (label.includes(string.toLowerCase())) {
                    markers.push(parseInt(el["Timestamp"]) / 1000);
                    frameUrls.push(el["FrameURL"]);
                }
            }
        }
        markers.forEach((i) => addMarker(video, i));

        // set up thumbnail frames
        frameUrls.forEach((e, i) =>
            addIm(i, markers[i], e, parseInt(_duration / 1000))
        );
        $("#search-images .thumbnail").hover(
            function () {
                $(this).find(".thumbnail-overlay").show();
            },
            function () {
                $(this).find(".thumbnail-overlay").hide();
            }
        );
    }

    function addTopwords() {
        for (var i = 0; i < _topwords.length; i++) {
            var word = $(
                `<span id=${i} class="each-topword">${_topwords[i]}</span>`
            );
            $("#topwords-list").append(word);
            word.click(function () {
                var id = $(this).attr("id");
                // console.log("word clicked", _topwords[id]);
                if (_treatment == 2) {
                    searchimages(_topwords[id]);
                }
            });
        }
    }

    addTopwords();

    // search video
    searchText.keyup(function () {
        clearMarkers();
        clearIms();
        var string = $(this).val();
        var markers = [];
        var frameUrls = [];
        if (string) {
            if (_treatment == 2) {
                // set up markers
                for (var i = 0; i < _data.length; i++) {
                    var el = _data[i];
                    var label = el["Label"]["Name"].toLowerCase();
                    var confidence = parseFloat(el["Label"]["Confidence"]);
                    if (confidence >= 97.5) {
                        if (label.includes(string.toLowerCase())) {
                            markers.push(parseInt(el["Timestamp"]) / 1000);
                            frameUrls.push(el["FrameURL"]);
                        }
                    }
                }
                markers.forEach((i) => addMarker(video, i));

                // set up thumbnail frames
                frameUrls.forEach((e, i) =>
                    addIm(i, markers[i], e, parseInt(_duration / 1000))
                );
                $("#search-images .thumbnail").hover(
                    function () {
                        $(this).find(".thumbnail-overlay").show();
                    },
                    function () {
                        $(this).find(".thumbnail-overlay").hide();
                    }
                );
            } else if (_treatment == 3) {
                // set up markers
                for (var i = 0; i < _data.length; i++) {
                    var el = _data[i];
                    var label =
                        el["TextDetection"]["DetectedText"].toLowerCase();
                    var confidence = parseFloat(
                        el["TextDetection"]["Confidence"]
                    );
                    if (confidence >= 97.5) {
                        if (label.includes(string.toLowerCase())) {
                            markers.push(parseInt(el["Timestamp"]) / 1000);
                            frameUrls.push(el["FrameURL"]);
                        }
                    }
                }
                markers.forEach((i) => addMarker(video, i));
            }
        }
    });
});
