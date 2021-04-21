'use strict';

$(document).ready(function() {

    let intervals = liquid;

    var player = videojs('my-video', {}, function onPlayerReady() {
            videojs.log('Your player is ready!');

            // set up 
            let currInterval = intervals[0];
            this.currentTime(currInterval["start"])

            // How about an event listener?
            this.on('stopped', function() {
                intervals = liquid; 
                videojs.log('Awww...over so soon?!');
            });
        }
    );

    function nextInterval() {
        intervals.shift(); // Shift() pops first element off array
        if (intervals.length > 0) {
            let currInterval = intervals[0];
            player.currentTime(currInterval["start"]);
        } else {
            player.pause();
        }
    }

    var id = setInterval(() => {
        if (intervals.length > 0) {
            let currInterval = intervals[0];
            if (currInterval["stop"] <= player.currentTime()) {
                nextInterval();
            }
        }
    }, 500);
});

/* 
 * EX. [(3, 9), (15, 42)]
 * checks:
 * - each number is less than the previous
 * - last number doesn't exceed the video duration
 */
