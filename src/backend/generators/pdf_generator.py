import markdown
from pathlib import Path
from typing import Any
from .document_generator import DocumentGenerator


class PDFGenerator(DocumentGenerator):
    """
    PDF document generator using Markdown to PDF conversion.

    Converts Markdown content to PDF using markdown and pdfkit.
    """

    async def generate(self, content: str, output_path: str, **kwargs: Any) -> bool:
        """
        Generate PDF document from Markdown content.

        Args:
            content: Markdown content
            output_path: Output PDF file path
            page_size: Optional page size (default: 'A4')
            margin_top: Optional top margin (default: '0.75in')
            margin_bottom: Optional bottom margin (default: '0.75in')
            margin_left: Optional left margin (default: '0.75in')
            margin_right: Optional right margin (default: '0.75in')

        Returns:
            True if PDF was created successfully
        """
        try:
            import pdfkit

            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            html = markdown.markdown(content)

            options = {
                "page-size": kwargs.get("page_size", "A4"),
                "margin-top": kwargs.get("margin_top", "0.75in"),
                "margin-bottom": kwargs.get("margin_bottom", "0.75in"),
                "margin-left": kwargs.get("margin_left", "0.75in"),
                "margin-right": kwargs.get("margin_right", "0.75in"),
                "encoding": "UTF-8",
            }

            pdfkit.from_string(html, output_path, options=options)

            return True
        except ImportError:
            print("pdfkit not installed. Please install it with: pip install pdfkit")
            print("Also install wkhtmltopdf: sudo apt-get install wkhtmltopdf")
            return False
        except Exception as e:
            print(f"Failed to generate PDF: {e}")
            return False
