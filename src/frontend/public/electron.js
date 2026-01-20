const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const http = require('http');

const API_BASE = 'http://localhost:8000';

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile('dist/index.html');
  }
}

ipcMain.handle('list-files', async (event, dirPath) => {
  try {
    const response = await fetch(`${API_BASE}/api/files/list/?path=${encodeURIComponent(dirPath)}`);
    const data = await response.json();
    return { success: true, files: data };
  } catch (error) {
    console.error('Failed to list files:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('read-file', async (event, filePath) => {
  try {
    const response = await fetch(`${API_BASE}/api/files/read/?path=${encodeURIComponent(filePath)}`);
    const data = await response.json();
    return { success: true, ...data };
  } catch (error) {
    console.error('Failed to read file:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('write-file', async (event, filePath, content) => {
  try {
    const response = await fetch(`${API_BASE}/api/files/write/?path=${encodeURIComponent(filePath)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    const data = await response.json();
    return { success: true, ...data };
  } catch (error) {
    console.error('Failed to write file:', error);
    return { success: false, error: error.message };
  }
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});