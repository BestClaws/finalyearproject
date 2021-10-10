$(document).ready(() => {

// hide all screens and their tabs except splash
$("#main_screen").hide();
$('#register_screen').hide();
$("#upload_tab").hide();
$("#packages_tab").hide();
$("#config_tab").hide();
$("#overlay").hide();

var fs = require('fs');


server_address = fs.readFileSync('data/server_address').toString();
user_name = fs.readFileSync('data/user_name').toString();

$("#display_name").html(user_name)


//hide splash screen momentarily
//show the next screen
$("#splash_screen").delay(1000).fadeOut(500, "swing", () => {
$('#upload_tab').show();
$('#main_screen').fadeIn(300);
});




});
