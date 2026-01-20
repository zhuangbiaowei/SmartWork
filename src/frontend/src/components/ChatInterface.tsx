import React, { useState } from 'react';

interface ChatInterfaceProps {
  selectedFile: any;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ selectedFile }) => {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([
    { role: 'assistant', content: '您好！我是 SmartWork AI 助手。有什么可以帮助您的吗？' }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || isProcessing) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    setIsProcessing(true);

    try {
      const response = await fetch('http://localhost:8000/api/tasks/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: input }),
      });

      const data = await response.json();

      if (data.success) {
        const aiMessage = {
          role: 'assistant',
          content: `任务已创建！任务 ID: ${data.task.id}\n状态: ${data.task.status}\n描述: ${data.task.description}`,
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        const errorMessage = {
          role: 'assistant',
          content: `创建任务失败: ${data.error || '未知错误'}`,
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `网络错误: ${error instanceof Error ? error.message : '未知错误'}`,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
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
          disabled={isProcessing}
        />
        <button onClick={handleSend} disabled={isProcessing}>
          {isProcessing ? '处理中...' : '发送'}
        </button>
      </div>
    </div>
  );
};