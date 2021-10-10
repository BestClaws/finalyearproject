

let remote = require('electron').remote;
let path = require('path');


// preview the list of selected files to upload
function preivew_files() {

    let updated_content = "";
    let filesListString = "";
    let no_of_files = $("#files_to_upload")[0].files.length;

    for(let x = 0; x < no_of_files; x++) {

        if ($("#files_to_upload")[0].files[x].type != "image/bmp") img_path = "assets/mime.png";
        else img_path = $("#files_to_upload")[0].files[x].path;

        updated_content += "<li>" + 
        "<img src='" +
        img_path +
        "' height='200px'>" +
        "</li>";


        $("#upload_files_list").html(updated_content);

    }

}



// TODO: make this a python service instead
function pack_files(files_list, package_name) {
    
    let files_list_string = "";
    
    for(let x = 0; x < files_list.length; x++)
        files_list_string += "'" + files_list[x] + "' ";

    let package_path = 'data/processing/' +  'package_' +  package_name + '_by_' + user_name + '.zip';

    let command = 'zip -r -j ' + package_path + ' ' + files_list_string;
    
    console.log('executing: ' + command)
    execute(command, (output) => {
      console.log(output);
      
    });

    return package_path;

}


// get a list of all files selected (gives their full paths as list)
function get_files_list() {

    let files_list = [];

    for(let x = 0; x < $("#files_to_upload")[0].files.length; x++)
        files_list.push($("#files_to_upload")[0].files[x].path);

    return files_list;

}



function upload_package() {

 



    box = $(".box");
    box_content = $(".box #box_content");
    overlay = $("#overlay");


    box_content.html('<img src="assets/loading.gif" width="50px" height="50px">')

    overlay.fadeIn(200, () => {

        // grab the package name
        let package_name = $("#upload_package_name")[0].value;
        // grab the files list
        let files_list = get_files_list();
        // package the files
        let package_path = pack_files(files_list, package_name);

        execute("python3 services/upload_package.py" +
            " " +
            user_name +
            " " + 
            package_name +
            " " + 
            package_path +
            " " + 
            server_address + "/upload_package",
         
            (output) => {
                console.log( output);
                overlay.fadeOut(200);
            }
        );



    });



}


$("#files_to_upload")[0].addEventListener('change', preivew_files, false);
$("#upload_package_btn")[0].addEventListener('click', upload_package, false);

$("")




