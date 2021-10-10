

if(typeof require != "undefined") { // nodejs is compatible


let remote = require('electron').remote;
let path = require('path');

// menu bar buttons event configuration

document.getElementById("close_app").addEventListener("click", function (e) {
var window = remote.getCurrentWindow();
window.close(); 
});

document.getElementById("minimize_app").addEventListener("click", function (e) {
var window = remote.getCurrentWindow();
window.minimize();

});

document.getElementById("maximize_app").addEventListener("click", function (e) {
var window = remote.getCurrentWindow();
if (!window.isMaximized()) {
  window.maximize();          
} else {
  window.unmaximize();
}
});


}