const API_BASE = 'http://localhost:8000/api';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000;

function isCacheValid(entry: { data: any; timestamp: number }): boolean {
  return Date.now() - entry.timestamp < CACHE_DURATION;
}

export const apiClient = {
  async listFiles(path: string = '.') {
    const cacheKey = `files:${path}`;

    const cached = cache.get(cacheKey);
    if (cached && isCacheValid(cached)) {
      return cached.data;
    }

    const response = await fetch(`${API_BASE}/files/list/?path=${path}`);
    const data = await response.json();

    if (data.success && data.files) {
      cache.set(cacheKey, {
        data: data.files,
        timestamp: Date.now(),
      });
    }

    return data.files;
  },

  async createTask(description: string) {
    const cacheKey = `task:create:${description}`;
    const timestamp = Date.now().toString();

    const response = await fetch(`${API_BASE}/tasks/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });

    const data = await response.json();

    if (data.success && data.task) {
      cache.set(cacheKey, {
        data: data.task,
        timestamp: Date.now(),
      });
    }

    return data;
  },

  async getTask(taskId: string) {
    const cacheKey = `task:${taskId}`;

    const cached = cache.get(cacheKey);
    if (cached && isCacheValid(cached)) {
      return cached.data;
    }

    const response = await fetch(`${API_BASE}/tasks/${taskId}`);
    const data = await response.json();

    if (data.success && data.task) {
      cache.set(cacheKey, {
        data: data.task,
        timestamp: Date.now(),
      });
    }

    return data;
  },

  async executeTask(taskId: string) {
    const response = await fetch(`${API_BASE}/tasks/${taskId}/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    return await response.json();
  },

  async getTaskState(taskId: string) {
    const response = await fetch(`${API_BASE}/tasks/${taskId}/state`);
    return await response.json();
  },

  async getTaskLogs(taskId: string) {
    const response = await fetch(`${API_BASE}/tasks/${taskId}/logs`);
    return await response.json();
  },

  async cancelTask(taskId: string) {
    const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    });

    cache.forEach((value, key) => {
      if (key.startsWith(`task:${taskId}`)) {
        cache.delete(key);
      }
    });

    return await response.json();
  },

  clearCache(): void {
    cache.clear();
  },

  getCacheStats(): { size: number; keys: string[] } {
    return {
      size: cache.size,
      keys: Array.from(cache.keys()),
    };
  },
};
