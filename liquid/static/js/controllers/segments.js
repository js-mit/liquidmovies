'use strict';

$(document).ready(function() {
    var progressContainer = $("#progress-container");
    var speakersContainer = $("#speakers-container");
    var segmentsContainer = $("#segments-container");

    for (const [key, value] of Object.entries(_data)) {
        var name = "";
        if (key=="spk_0") {
            name = "Tucker Carlson";
        } else if (key=="spk_1") {
            name = "Hannah Beth-Jackson";
        } else if (key=="spk_2") {
            name = "Jason Nicolas";
        } else {
            name = key;
        }
        speakersContainer.append($(`<button class="speaker-btn" id="${key}">${name}</button>`));
    }

    $(".speaker-btn").each(function() {
        var speaker = $(this).attr("id");
        $(this).click(function() {
            segmentsContainer.empty();
            var segments = _data[speaker];
            for (var i=0; i<segments.length; i++) {
                var start = segments[i]["start_time"];
                var end = segments[i]["end_time"];
                createSegment(start, end);
            }
            play(segments);
        });
    });

    function createSegment(start, end) {
        var segment = $(`<div class="segment"></div>`);
        segment.css("left", 100*start/_duration + "%");
        segment.css("width", 100*(end-start)/_duration + "%");
        segmentsContainer.append(segment);
    }

    function play(segments) {
        console.log(segments);
        var video = $("#video");
        var start = segments[0]["start_time"];
        var end = segments[0]["end_time"];
        var wait = true;
        video.prop("currentTime", Math.round(start/1000));
        video.trigger("play");
        const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
        (async function loop() {
            while (wait) {
                await delay(500);
                if (video.prop("currentTime") > end/1000) {
                    wait = false;
                    video.trigger("pause")
                    if (segments.length > 1) {
                        play(segments.slice(1));
                    }
                }
            }
        })();
    }


    // function createSegments(liquid) {
    //     var segments = []
    //     var start = 0;
    //     var end = 0;
    //     var curr = false;
    //     for (var i = 0; i < liquid.length; i++) {
    //         if (liquid[i]==1 && curr==false) {
    //             curr = true;
    //             start = i;
    //         }
    //         if (liquid[i]==0 && curr==true) {
    //             curr = false;
    //             end = i - 1;
    //             segments.push([start, end]);
    //         }
    //     }
    //     if (curr==true) {
    //         end = liquid.length;
    //         segments.push([start, end]);
    //     }
    //     return segments
    // }
    // console.log(createSegments(liquid));

});
