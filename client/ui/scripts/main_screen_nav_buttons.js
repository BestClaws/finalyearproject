// current tab name
let current_tab = 'upload_tab';



function navigate_to_tab(new_tab) {

    let current_tab_id = '#' + current_tab;   
    let new_tab_id = '#' + new_tab;
    
    // ignore if clicked on the same tab
    if(current_tab_id == new_tab_id) return false;

    // remove active tab attribute from current tab and 
    $("#main_screen_nav_buttons").find("[active_tab]").removeAttr('active_tab');
    $("#main_screen_nav_buttons").find('[' + new_tab + ']').attr('active_tab', '');


    $(current_tab_id).fadeOut(200, "swing", () => {
        $(new_tab_id).fadeIn(200);
        current_tab = new_tab;


        // other processing
        if(current_tab == 'config_tab') {
            console.log('retieving config info...')
            retrieve_config_info();
        }

    });


    
}