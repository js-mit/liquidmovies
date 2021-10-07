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
    playpause.click(function(e) {
        if (video.prop("paused") || video.prop("ended")) {
            video.trigger("play");
            playIcon.hide();
            pauseIcon.show();
        } else {
            video.trigger("pause");
            playIcon.show();
            pauseIcon.hide();
        }
    });

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
        video.currentTime = pos * video.prop("duration");
    }); 

    // timestamp
    duration.html(renderTime(video.prop("duration"), video.prop("duration")));
    function renderTime(seconds, duration) {
        var t = new Date(seconds * 1000).toISOString();
        return (duration < 3600) ? t.substr(14, 5) : t.substr(11, 8);
    }
    video.on("timeupdate", function() {
        $(currentTime).html(renderTime(video.prop("currentTime"), video.prop("duration")));
    });

});

// $(document).ready(function() {
// 
//     // taken from jinja2
//     let intervals = liquid;
// 
//     // set up video
//     var player = videojs("my-video', {}, function onPlayerReady() {
//         videojs.log("Your player is ready!");
// 
//         // How about an event listener?
//         this.on("stopped', function() {
//             intervals = liquid;
//         });
//     });
// 
//     // bookmarker
//     if (method==1) {
//         player.currentTime(intervals[0]["start"]);
//         setupPlayIntervals(intervals, player);
//     }
//     // diarization
//     else if (method==2) {
//         let speakers = intervals;
//         for (const [key, value] of Object.entries(intervals)) {
//             var btn = `<button class='speaker' data-speaker='${key}'>${key}</button>`;
//             $(".controls").append(btn);
//             var field = `${key} : <input type='text' data-key="${key}"></input><br>`;
//             $(".update-speakers").append(field);
//         }
// 
//         $(".controls .speaker").each(function() {
//             $(this).click(function() {
//                 let speaker = $(this).data("speaker");
//                 player.currentTime(speakers[speaker][0]["start"]);
//                 setupPlayIntervals(speakers[speaker], player);
//             });
//         });
// 
//         $(".submit-new-speakers").click(() => {
//             let updatedSpeakers = {};
//             $(".update-speakers").children("input").each(function() {
//                 let oldKey = $(this).data("key");
//                 let newKey = $(this).val();
//                 updatedSpeakers[oldKey] = newKey;
//             });
//             let postUrl = $(".submit-new-speakers").data("action");
// 
//             $.post(postUrl, {
//                 "mapping": JSON.stringify(updatedSpeakers),
//                 "desc": "test"
//             }, function(data) {
//                 window.location.replace(data);
//             })
//             .fail(function() {
//                 alert("error");
//             });
//         });
//     }
// 
// });
// 
// function setupPlayIntervals(intervals, player) {
//     let _intervals = JSON.parse(JSON.stringify(intervals));
// 
//     $(".control-next").click(nextInterval);
// 
//     function nextInterval() {
//         _intervals.shift(); // Shift() pops first element off array
//         if (intervals.length > 0) {
//             let currInterval = _intervals[0];
//             player.currentTime(currInterval["start"]);
//         } else {
//             player.pause();
//         }
//     }
// 
//     var id = setInterval(() => {
//         if (intervals.length > 0) {
//             let currInterval = _intervals[0];
//             if (currInterval["stop"] <= player.currentTime()) {
//                 nextInterval();
//             }
//         }
//     }, 100);
// }
