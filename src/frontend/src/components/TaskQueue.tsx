import React from 'react';

interface Task {
  id: string;
  description: string;
  status: string;
  progress?: number;
}

interface TaskQueueProps {
  tasks: Task[];
}

export const TaskQueue: React.FC<TaskQueueProps> = ({ tasks }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return '#4CAF50';
      case 'in_progress': return '#2196F3';
      case 'failed': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  return (
    <div className="task-queue">
      <h3>任务队列</h3>
      
      <div className="task-list">
        {tasks.length === 0 ? (
          <p className="empty-state">暂无任务</p>
        ) : (
          tasks.map((task) => (
            <div key={task.id} className="task-item">
              <div className="task-header">
                <span className="task-title">{task.description}</span>
                <span 
                  className="task-status"
                  style={{ color: getStatusColor(task.status) }}
                >
                  {task.status}
                </span>
              </div>
              
              {task.progress !== undefined && (
                <div className="task-progress">
                  <div 
                    className="progress-bar"
                    style={{ width: `${task.progress}%` }}
                  />
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};