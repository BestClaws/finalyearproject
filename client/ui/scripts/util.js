// function execute(command, callback) {
//     const exec = require('child_process').execSync;
//     exec(command, (error, stdout, stderr) => { 
//         callback(' \nerr: ' + error + '\nstdout: \n' + stdout + '\nstderr: \n' + stderr + '\n'); 
//     });
// };

function execute(command, callback) {
    const exec = require('child_process').execSync;
    callback('stdout:\n' + exec(command));
};