import logging
import shutil
import jinja2
from pathlib import Path
from typing import List, Dict, Any

class LaTeXBuilder:
    def __init__(self, output_dir: Path):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja
        template_dir = Path(__file__).parent.parent / "templates"
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            variable_start_string='{{',
            variable_end_string='}}',
            comment_start_string='<#',
            comment_end_string='#>'
        )

    def build_book(self, book_title: str, chapters: List[Dict[str, Any]]):
        """
        Assemble the main.tex file.
        """
        self.logger.info(f"Building book: {book_title}")
        
        # 1. Create directory structure
        (self.output_dir / "Figures").mkdir(exist_ok=True)
        (self.output_dir / "Pictures").mkdir(exist_ok=True)
        
        # 2. Render main.tex
        template = self.env.get_template("main.tex.jinja2")
        rendered = template.render(
            book_title=book_title,
            chapters=chapters
        )
        
        main_file = self.output_dir / "main.tex"
        main_file.write_text(rendered)
        self.logger.info(f"Written main.tex to {main_file}")

    def build_chapter(self, chapter_data: Dict[str, Any]):
        """
        Write a single chapter file.
        chapter_data must include 'title', 'safe_title', 'content', 'file_name'
        """
        self.logger.info(f"Building chapter: {chapter_data['title']}")
        
        template = self.env.get_template("chapter.tex.jinja2")
        rendered = template.render(chapter=chapter_data)
        
        # Remove extension from file_name if present for write, 
        # but usage in main.tex typically assumes file without extension or with it.
        # Let's assume file_name has .tex
        
        out_file = self.output_dir / chapter_data['file_name']
        out_file.write_text(rendered)

    def write_bibliography(self, bib_content: str):
        bib_file = self.output_dir / "bibliography.bib"
        bib_file.write_text(bib_content)
