/*******************************************************************************

    CUSTOM COMMON FUNCTIONS.

*******************************************************************************/

// Generate flash message.
function flash_message(category, message) {
    var message_element = document.createElement('div');
    message_element.className = "alert alert-" + category + " alert-dismissible";
    var message_button = $.parseHTML('<button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span></button>');
    message_element.appendChild(message_button[0]);
    var message_text = document.createTextNode(message);
    message_element.appendChild(message_text);
    $(".container-flashed-messages").append(message_element);
}
