var packages = [];


$("#search_query").on('change', search_packages);
$("#refresh_packages_btn").on('click', refresh_packages);


// update package cache
function refresh_packages() {

        console.log('refreshing...');
    
        fetch(server_address + '/list_packages?user_name=' + user_name)
            .then((res) => {
                return res.json();
            })
            .then((res_packages) => {
                console.log(res_packages);
                packages  = res_packages;
            });

        search_packages();
}

// search from the cached packages list and show results
function search_packages() {

    query = $("#search_query")[0].value;

    let updated_content = 
    "\
    <tr>\
    <th>Name</th>\
    <th>Owner</th>\
    <th>Original</th>\
    <th>Compressed</th>\
    <th>Dropped by</th>\
    <th>Processed In</th>\
    <th>Actions</th>\
    </tr>" ;

    $("#packages_list").fadeOut(200, "swing", () => {



        for(let x = 0; x < packages.length; x++) {

            if(packages[x].package_name.toLowerCase().includes(query.toLowerCase())) {

                updated_content += 

        
                    '<tr>' +
                      '<td>' + packages[x].package_name + '</td>' +
                      '<td>' + packages[x].package_owner + '</td>' +
                      
                      '<td>' + packages[x].original_size.toPrecision(4) + ' KB</td>' +
                      '<td>' + packages[x].compressed_size.toPrecision(4) + 'KB</td>' +
                      '<td>' + (100 - ((packages[x].compressed_size / packages[x].original_size) * 100).toPrecision(3)) + '%</td>' +
                      '<td>' + packages[x].processing_time.toPrecision(4) + 'ms</td>' +

                      '<td><ul class="buttons">' +
                        
                        '<li onclick="ps(); send_package(\'' + packages[x].package_name + '\');">' +
                          '<ion-icon name="ios-send"></ion-icon>' +
                        '</li>' +
                        
                        
                        '<li onclick="ps(); download_package(\'' + packages[x].package_name + '\');">' +
                          '<ion-icon name="ios-download"></ion-icon>' + 
                        '</li>' +
                        
                        
                        '<li onclick="ps(); delete_package(\'' + packages[x].package_name + '\');">' +
                          '<ion-icon name="ios-trash"></ion-icon>' +
                        '</li>' +
                        
                        

                      '</ul></td>' + 
                    '</tr>'
            }

        }

        $('#packages_list').html(updated_content);

        $("#packages_list").fadeIn(200);


    });




}

function delete_package(package_name) {

console.log('trying to delete: ' + package_name);
fetch(server_address + '/delete_package?user_name=' + user_name + '&package_name=' + package_name)
    .then((res) => {
        console.log(res);
        console.log('deleted');
        refresh_packages();
    })
    .then((x) => {
    });

}

function download_package(package_name) {

    console.log('trying to download: ' + package_name);
    fetch(server_address + '/download_package?user_name=' + user_name + '&package_name=' + package_name)
        .then((res) => {
            console.log("server response: ");
            console.log(res);
            console.log('link generated...');
            console.log('executing local post download steps...');
            execute('python3 services/download_package.py ' + 'package_' + package_name + '_by_' + user_name + '.zip', (res) => {
                console.log(res);
                console.log("done");
            });
            
        })
        .then((x) => {
        });
    
}

function send_package(package_name) {
    
    form_html = '\
    <input id="target_user" placeholder="User Name" name="id">\
    <button id="send_package_btn" onclick="ps(); send_package_next(\'' + package_name + '\')">Send</button>\
    ';

    box = $(".box").show();
    box_content = $(".box #box_content").show();
    overlay = $("#overlay");

    box_content.html(form_html) // fill the box with form
    box.attr("style", ''); // reset box dimensions



    $("#overlay").fadeIn();
}

function send_package_next(package_name) {
    
    target_user = $("#target_user")[0].value;

    box = $(".box");
    box_content = $(".box #box_content");
    overlay = $("#overlay")

    box_content.animate({"opacity": 0}, 200, () => {


        box.animate({"width": 50, "height": 50}, 500,() => {
        
            box_content.html('<img src="assets/loading.gif" width="50px" height="50px">');

            // send the package here...
            fetch(server_address + '/send_package?user_name=' + user_name + '&package_name=' + package_name + '&target_user=' + target_user + '&stage=one')
                .then((res) => {
                    console.log(res);
                    return res.json();
                })
                .then((res) => {
                    console.log(res);

                    var fs = require("fs");

                    fs.writeFile('data/processing/send_temp', JSON.stringify(res), function(err) {
                        if (err) {
                            return console.error(err);
                        }
                        
                        console.log("Data written successfully!");

                        execute('python3 services/send_package.py ' + user_name + ' ' + target_user + ' ' + package_name, (res) => {
                            console.log(res);
                            console.log("done");
                        });

        

                    });
                });


            box_content.animate({"opacity": 1}, 200, () => {

                box_content.animate({"opacity": 0}, 200, () => {
                    box.animate({"width": 300, "height": 300}, 500, () => {
                        box_content.html("<div style='height: 100%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 50px;'>Sent!</div>");
                        box_content.animate({"opacity": 1}, 200, () => {

                            box.delay(1000).fadeOut(100, "swing", () => {
                                overlay.delay(100).fadeOut();
                            });

                        });
                    });
                });

            });

        });
    });
}




