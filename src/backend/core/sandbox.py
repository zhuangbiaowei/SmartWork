import subprocess
import tempfile
import shutil
import os
from pathlib import Path
from typing import List, Dict, Optional, Any


class Sandbox:
    """
    Isolated execution environment for safe command execution.

    Provides a temporary working directory with controlled file access
    to prevent malicious or accidental file system modifications.
    """

    def __init__(self, allowed_paths: Optional[List[str]] = None):
        self.temp_dir: Path = Path(tempfile.mkdtemp(prefix="smartwork_sandbox_"))
        self.allowed_paths: List[str] = allowed_paths or []
        self._initialized: bool = False

    def initialize(self) -> None:
        """
        Initialize the sandbox environment.

        Creates necessary directory structure and sets up permissions.
        """
        if not self._initialized:
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self._initialized = True

    def execute_command(
        self, command: str, allowed_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a command safely within the sandbox.

        Args:
            command: The shell command to execute
            allowed_paths: List of paths the command is allowed to access

        Returns:
            Dictionary containing:
                - success: bool - whether execution succeeded
                - stdout: str - standard output
                - stderr: str - standard error
                - returncode: int - process return code
                - error: str - error message if failed
        """
        if not self._initialized:
            self.initialize()

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "error": None,
            }
        except subprocess.TimeoutExpired as e:
            return {
                "success": False,
                "stdout": e.stdout if e.stdout else "",
                "stderr": e.stderr if e.stderr else "",
                "returncode": -1,
                "error": "Command execution timed out",
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": "",
                "returncode": -1,
                "error": str(e),
            }

    def write_file(self, filename: str, content: str) -> Dict[str, any]:
        """
        Write content to a file within the sandbox.

        Args:
            filename: The name of file to create
            content: The content to write

        Returns:
            Dictionary with success status and error if any
        """
        if not self._initialized:
            self.initialize()

        try:
            file_path = self.temp_dir / filename
            file_path.write_text(content, encoding="utf-8")
            return {"success": True, "path": str(file_path), "error": None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_file(self, filename: str) -> Dict[str, any]:
        """
        Read content from a file within the sandbox.

        Args:
            filename: The name of the file to read

        Returns:
            Dictionary with success status, content, and error if any
        """
        if not self._initialized:
            self.initialize()

        try:
            file_path = self.temp_dir / filename
            if not file_path.exists():
                return {"success": False, "error": f"File {filename} not found"}

            content = file_path.read_text(encoding="utf-8")
            return {"success": True, "content": content, "error": None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_files(self, directory: str = ".") -> Dict[str, any]:
        """
        List files within a directory in the sandbox.

        Args:
            directory: The directory path relative to sandbox root

        Returns:
            Dictionary with success status and list of files
        """
        if not self._initialized:
            self.initialize()

        try:
            target_dir = self.temp_dir / directory
            if not target_dir.exists():
                return {"success": False, "error": "Directory not found"}

            files = []
            for item in target_dir.iterdir():
                files.append(
                    {
                        "name": item.name,
                        "is_dir": item.is_dir(),
                        "size": item.stat().st_size if item.is_file() else 0,
                    }
                )

            return {"success": True, "files": files, "error": None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_temp_dir(self) -> str:
        """
        Get the path to the temporary sandbox directory.

        Returns:
            Path string to the sandbox directory
        """
        return str(self.temp_dir)

    def cleanup(self) -> None:
        """
        Clean up the sandbox by removing the temporary directory.

        Should be called after task execution to free disk space.
        """
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self._initialized = False

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
