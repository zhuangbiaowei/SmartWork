import { useState, useEffect } from 'react';
import { FileBrowser } from './components/FileBrowser';
import { TaskQueue } from './components/TaskQueue';
import { ChatInterface } from './components/ChatInterface';
import './App.css';

interface FileItem {
  name: string;
  is_dir: boolean;
  size: number;
}

declare global {
  interface Window {
    electronAPI?: {
      listFiles: (path: string) => Promise<{ success: boolean; files?: FileItem[]; error?: string }>;
      readFile: (path: string) => Promise<{ success: boolean; content?: string; error?: string }>;
      writeFile: (path: string, content: string) => Promise<{ success: boolean; error?: string }>;
    };
  }
}

function App() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [_tasks] = useState([]);
  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);

  useEffect(() => {
    const electronAvailable = window.electronAPI !== undefined;

    if (electronAvailable) {
      loadFiles();
    }
  }, []);

  const loadFiles = async () => {
    if (!window.electronAPI) return;

    try {
      const result = await window.electronAPI.listFiles('.');
      if (result.success) {
        setFiles(result.files || []);
      } else {
        console.error('Failed to load files:', result.error);
      }
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
            onFileSelect={(file) => setSelectedFile(file)}
            onRefresh={loadFiles}
          />
        </div>

        <div className="content">
          <TaskQueue tasks={[]} />
        </div>

        <div className="chat-panel">
          <ChatInterface selectedFile={selectedFile} />
        </div>
      </main>
    </div>
  );
}

export default App;