import pytest
from slides_to_textbook.modules.latex_components import MarginNoteGenerator, BibliographyManager

def test_margin_note_simple():
    gen = MarginNoteGenerator()
    note = gen.generate_note("This is a note.")
    assert "\\automarginnote{This is a note.}}" in note

def test_margin_note_with_image():
    gen = MarginNoteGenerator()
    note = gen.generate_note("Bio", "/path/to/img.jpg", "Caption")
    assert "\\includegraphics[width=\\linewidth]{img.jpg}" in note
    assert "\\textbf{Caption}" in note

def test_bib_manager_add_entry():
    bib = BibliographyManager()
    entry = {
        "title": "A Paper",
        "author": ["John Doe"],
        "year": "2023",
        "entry_type": "article"
    }
    key = bib.add_entry(entry)
    assert key == "Doe2023"
    assert len(bib.entries) == 1

def test_bib_generate():
    bib = BibliographyManager()
    bib.add_entry({
        "title": "A Paper",
        "author": ["John Doe"],
        "year": "2023",
        "entry_type": "article"
    })
    content = bib.generate_bibtex()
    assert "@article{Doe2023," in content
    assert "title = {A Paper}," in content
