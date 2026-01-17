import React, { useState, useEffect } from 'react';
import { FileBrowser } from './components/FileBrowser';
import { TaskQueue } from './components/TaskQueue';
import { ChatInterface } from './components/ChatInterface';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const fileData = await window.electronAPI.listFiles('.');
      setFiles(fileData.files || []);
    } catch (error) {
      console.error('Failed to load files:', error);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>SmartWork - AI 智能体协作平台</h1>
      </header>
      
      <main className="app-main">
        <div className="sidebar">
          <FileBrowser 
            files={files} 
            onFileSelect={setSelectedFile}
            onRefresh={loadFiles}
          />
        </div>
        
        <div className="content">
          <TaskQueue tasks={tasks} />
        </div>
        
        <div className="chat-panel">
          <ChatInterface selectedFile={selectedFile} />
        </div>
      </main>
    </div>
  );
}

export default App;