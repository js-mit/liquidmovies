var maxField = 10; //Input fields increment limitation
var addButton = $('.add_button'); //Add button selector
var wrapper = $('.wrapper'); //Input field wrapper
var submitButton = $('.submit'); 
var fieldHTML = `
    <div class="bookmark">
        Start | Stop: 
        <input type="number" name="start_time" value="" onkeypress="return validate(event)"/>
        <input type="number" name="stop_time" value="" onkeypress="return validate(event)"/>
        <span class="remove_button">(remove)</span>
    </div>
`;
var response = $('.response');
var x = 1; //Initial field counter is 1
    
$(document).ready(() => {

    //Once add button is clicked
    addButton.click(() => {
        if(x < maxField){ 
            x++; //Increment field counter
            wrapper.append(fieldHTML); 
        }
    });
    
    //Once remove button is clicked
    wrapper.on('click', '.remove_button', (e) => {
        $(this).parent('div').remove(); //Remove field html
        x--; //Decrement field counter
    }); 

    //Submit form
    submitButton.click(() => {
        body = getBookmarks();
        postUrl = submitButton.data("action");

        $.post(postUrl, {
            "bookmarks": JSON.stringify(body)
        }, function(data) {
            console.log(data);
            window.location.replace(data);
        });
    });
});

/**
 * Checks that all the inputs are valid (stop times can't be bigger than start
 * times, and each subsequent bookmark can't be before previous ones). Returns
 * the bookmarks as a list: [{"start": 1, "stop": 3}, {"start": 4, "stop": 7}]
 */
function getBookmarks() {
    var counter = 0;
    var body = [];
    $(".bookmark").each(function() {
        let start = parseInt($(this).find("input[name='start_time']").val());
        let stop = parseInt($(this).find("input[name='stop_time']").val());
        if (counter > start || start > stop) {
            response.html("error");
            return false;
        }
        body.push({"start": start, "stop": stop})
        counter = stop;
    });
    return body
};


function validate(evt) {
    var theEvent = evt || window.event;

    // Handle paste
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
        // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if( !regex.test(key) ) {
        theEvent.returnValue = false;
        if(theEvent.preventDefault) theEvent.preventDefault();
    }
}


