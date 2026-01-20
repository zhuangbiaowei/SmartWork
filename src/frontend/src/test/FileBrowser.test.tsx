import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FileBrowser } from '../components/FileBrowser';

describe('FileBrowser', () => {
  const mockFiles = [
    { name: 'test.txt', is_dir: false, size: 1024 },
    { name: 'docs', is_dir: true, size: 0 },
    { name: 'report.pdf', is_dir: false, size: 2048 },
  ];

  it('renders file list correctly', () => {
    const onFileSelect = vi.fn();
    const onRefresh = vi.fn();

    render(
      <FileBrowser
        files={mockFiles}
        onFileSelect={onFileSelect}
        onRefresh={onRefresh}
      />
    );

    expect(screen.getByText('文件浏览器')).toBeInTheDocument();
    expect(screen.getByText('test.txt')).toBeInTheDocument();
    expect(screen.getByText('docs')).toBeInTheDocument();
    expect(screen.getByText('report.pdf')).toBeInTheDocument();
  });

  it('calls onRefresh when refresh button clicked', () => {
    const onRefresh = vi.fn();
    const onFileSelect = vi.fn();

    render(
      <FileBrowser
        files={mockFiles}
        onFileSelect={onFileSelect}
        onRefresh={onRefresh}
      />
    );

    const refreshButton = screen.getByText('刷新');
    refreshButton.click();

    expect(onRefresh).toHaveBeenCalledTimes(1);
  });

  it('calls onFileSelect when file is clicked', () => {
    const onFileSelect = vi.fn();
    const onRefresh = vi.fn();

    render(
      <FileBrowser
        files={mockFiles}
        onFileSelect={onFileSelect}
        onRefresh={onRefresh}
      />
    );

    const fileItem = screen.getByText('test.txt');
    fileItem.click();

    expect(onFileSelect).toHaveBeenCalledWith(mockFiles[0]);
  });

  it('displays empty state when no files', () => {
    const onFileSelect = vi.fn();
    const onRefresh = vi.fn();

    render(
      <FileBrowser
        files={[]}
        onFileSelect={onFileSelect}
        onRefresh={onRefresh}
      />
    );

    expect(screen.queryByText('test.txt')).not.toBeInTheDocument();
  });
});
