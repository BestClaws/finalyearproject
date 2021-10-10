function update_config_info(form) {
    server_address = form.form.server_address.value; 

    var fs = require('fs');

    fs.writeFileSync('data/server_address', server_address)

    
}

function create_user(form) {
    user_name = form.form.user_name.value;

    var fs = require('fs');

    fs.writeFileSync('data/user_name', user_name)

 
    execute('echo y | ssh-keygen -t rsa -C "'+  user_name+  '" -f data/key -N ""', (res) => {
        console.log(res);
        console.log('created key succesfully');


        pub_key = fs.readFileSync('data/key.pub').toString();
        console.log('pub key is: ' + pub_key)

        fetch(server_address + '/create_user', {
            method: 'post',
            headers: {
              'Accept': 'application/json, text/plain, */*',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({user_name: user_name, pub_key: pub_key})
          }).then(res=>res.json())
            .then(res => {
                console.log('user created...');
                console.log(res)
            });

    })


    $("#display_name").html(user_name)
}  

function retrieve_config_info() {

    form = $("#config_form")[0]


    form.user_name.value = user_name
    form.server_address.value = server_address


}