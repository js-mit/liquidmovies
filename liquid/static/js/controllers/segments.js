'use strict';

$(document).ready(function() {
    var progressContainer = $("#progress-container");

    function createSegments(liquid) {
        var segments = []
        var start = 0;
        var end = 0;
        var curr = false;
        for (var i = 0; i < liquid.length; i++) {
            if (liquid[i]==1 && curr==false) {
                curr = true;
                start = i;
            }
            if (liquid[i]==0 && curr==true) {
                curr = false;
                end = i - 1;
                segments.push([start, end]);
            }
        }
        if (curr==true) {
            end = liquid.length;
            segments.push([start, end]);
        }
        return segments
    }
    console.log(createSegments(liquid));

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
