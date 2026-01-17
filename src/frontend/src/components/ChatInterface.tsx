import React, { useState } from 'react';

interface ChatInterfaceProps {
  selectedFile: any;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ selectedFile }) => {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([
    { role: 'assistant', content: '您好！我是 SmartWork AI 助手。有什么可以帮助您的吗？' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    
    setTimeout(() => {
      const aiMessage = { 
        role: 'assistant', 
        content: `收到您的消息: "${input}"。我正在处理中...` 
      };
      setMessages(prev => [...prev, aiMessage]);
    }, 500);

    setInput('');
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>AI 助手</h3>
        {selectedFile && (
          <span className="selected-file">当前文件: {selectedFile.name}</span>
        )}
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}
      </div>
      
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="输入您的需求..."
        />
        <button onClick={handleSend}>发送</button>
      </div>
    </div>
  );
};