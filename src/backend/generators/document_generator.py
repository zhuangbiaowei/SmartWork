from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class DocumentGenerator(ABC):
    """
    Abstract base class for document generators.

    Defines the interface for generating different document formats.
    """

    @abstractmethod
    async def generate(self, content: str, output_path: str, **kwargs: Any) -> bool:
        """
        Generate a document from content.

        Args:
            content: The content to generate document from
            output_path: Path where document should be saved
            **kwargs: Additional parameters for specific generators

        Returns:
            True if successful, False otherwise
        """
        pass


class MarkdownGenerator(DocumentGenerator):
    """
    Markdown document generator.

    Simple generator that saves Markdown content directly to a file.
    """

    async def generate(self, content: str, output_path: str, **kwargs: Any) -> bool:
        """
        Generate Markdown document.

        Args:
            content: Markdown content
            output_path: Output file path

        Returns:
            True if file was created successfully
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

            return True
        except Exception as e:
            print(f"Failed to generate Markdown: {e}")
            return False
