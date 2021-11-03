'use strict';

$(document).ready(function() {

    // check if the browser actually supports the <video> element
    var supportsVideo = !!document.createElement("video").canPlayType;
    if (!supportsVideo) throw "browser does not support video";

    var videoContainer = $("#video-container");
    var video = $("#video");
    var videoControls = $("#video-controls");
    var playpause = $("#playpause");
    var playIcon = $("#playpause>#play");
    var pauseIcon = $("#playpause>#pause");
    var stop = $("#stop");
    var mute = $("#mute");
    var volinc = $("#volinc");
    var voldec = $("#voldec");
    var progress = $("#progress");
    var progressBar = $("#progress-bar");
    var timestamp = $("#timestamp");
    var currentTime = $("#current-time");
    var duration = $("#duration");

    // Hide the default controls
    video.prop("controls", false);

    // Display the user defined video controls
    videoControls.show();

    // Play / Pause
    pauseIcon.hide();
    playpause.click(togglePlayPause);
    video.click(togglePlayPause);
    function togglePlayPause() {
        if (video.prop("paused") || video.prop("ended")) {
            video.trigger("play");
            playIcon.hide();
            pauseIcon.show();
        } else {
            video.trigger("pause");
            playIcon.show();
            pauseIcon.hide();
        }
    }

    // Stop
    stop.click(function(e) {
        video.trigger("pause");
        video.prop("currentTime", 0);
        progress.prop("value", 0);
    });

    // Mute
    mute.click(function(e) {
        video.prop("muted") = !video.prop("muted");
    });

    // Volume
    volinc.click(function(e) {
        alterVolume("+");
    });
    voldec.click(function(e) {
        alterVolume("-");
    });
    var alterVolume = function(dir) {
        var currentVolume = Math.floor(video.prop("volume") * 10) / 10;
        if (dir === "+") {
            if (currentVolume < 1) video.prop("volume") += 0.1;
        }
        else if (dir === "-") {
            if (currentVolume > 0) video.prop("volume") -= 0.1;
        }
    }

    // Progress bar
    video.on("loadedmetadata", function() {
        progress.attr("max", video.prop("duration"));
    });

    video.on("timeupdate", function() {
        if (!progress.attr("max")) progress.attr("max", video.prop("duration"));
        progress.prop("value", video.prop("currentTime"));
        progressBar.width(Math.floor((video.prop("currentTime") / video.prop("duration") * 100) + "%"));
    });

    // skip ahead
    progress.click(function(e) {
        var rect = this.getBoundingClientRect();
        var pos = (e.pageX  - rect.left) / this.offsetWidth;
        video.prop("currentTime", pos * video.prop("duration"));
    });

    // timestamp
    duration.html(renderTime(video.prop("duration"), video.prop("duration")));

    video.on("timeupdate", function() {
        $(currentTime).html(renderTime(video.prop("currentTime"), video.prop("duration")));
    });

});

