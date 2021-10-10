const {app, BrowserWindow} = require('electron');

function createWindow () {

	win = new BrowserWindow({
		width: 1280,
		height: 720,
		frame: false,
		show: false,
		webPreferences: {
			nodeIntegration: true,
			webSecurity: false
		}
	});
//	win.loadURL('http://localhost:8080');
  win.loadFile('ui/index.html');

	win.once('ready-to-show', () => {
		win.show()
	})

}




app.on('ready', createWindow);
