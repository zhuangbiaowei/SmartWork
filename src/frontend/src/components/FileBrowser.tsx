import React from 'react';

interface File {
  name: string;
  is_dir: boolean;
  size: number;
}

interface FileBrowserProps {
  files: File[];
  onFileSelect: (file: File | null) => void;
  onRefresh: () => void;
}

export const FileBrowser: React.FC<FileBrowserProps> = ({ files, onFileSelect, onRefresh }) => {
  return (
    <div className="file-browser">
      <div className="file-browser-header">
        <h3>文件浏览器</h3>
        <button onClick={onRefresh}>刷新</button>
      </div>
      
      <div className="file-list">
        {files.map((file, index) => (
          <div 
            key={index}
            className="file-item"
            onClick={() => onFileSelect(file)}
          >
            <span className="file-icon">
              {file.is_dir ? '📁' : '📄'}
            </span>
            <span className="file-name">{file.name}</span>
            <span className="file-size">
              {file.is_dir ? '-' : `${file.size} bytes`}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};