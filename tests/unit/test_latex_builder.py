import pytest
import shutil
from pathlib import Path
from slides_to_textbook.modules.latex_builder import LaTeXBuilder

@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "book_out"

@pytest.fixture
def builder(output_dir):
    return LaTeXBuilder(output_dir)

def test_build_chapter(builder, output_dir):
    chapter_data = {
        "title": "Intro",
        "safe_title": "Intro",
        "content": "Hello World",
        "file_name": "Chapter-Intro.tex"
    }
    
    builder.build_chapter(chapter_data)
    
    assert (output_dir / "Chapter-Intro.tex").exists()
    content = (output_dir / "Chapter-Intro.tex").read_text()
    assert "\\chapter{ Intro }" in content
    assert "Hello World" in content

def test_build_book(builder, output_dir):
    chapters = [
        {"file_name": "Chapter-1"},
        {"file_name": "Chapter-2"}
    ]
    
    builder.build_book("ML Book", chapters)
    
    assert (output_dir / "main.tex").exists()
    content = (output_dir / "main.tex").read_text()
    assert "\\title{ ML Book }" in content
    assert "\\include{ Chapter-1 }" in content

def test_write_bib(builder, output_dir):
    builder.write_bibliography("test")
    assert (output_dir / "bibliography.bib").read_text() == "test"
