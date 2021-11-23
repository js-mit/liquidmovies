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
