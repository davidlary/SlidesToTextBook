from typing import List, Dict, Any

class MarginNoteGenerator:
    def generate_note(self, content: str, image_path: str = "", caption: str = "") -> str:
        """
        Create a LaTeX margin note command.
        """
        note = "\\automarginnote{"
        if image_path:
            # Assuming image path is relative or handled by graphicspath in main.tex
            # taking basename for safety if handled elsewhere
            import os
            base = os.path.basename(image_path)
            note += f"\\includegraphics[width=\\linewidth]{{{base}}}\\\\ "
        
        if caption:
            note += f"\\textbf{{{caption}}} "
            
        note += content + "}}"
        return note

    def generate_person_note(self, person_name: str, bio: str, image_path: str) -> str:
        return self.generate_note(bio, image_path, person_name)


class BibliographyManager:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: Dict[str, Any]):
        """
        Add a citation entry.
        entry dict should have: entry_type, title, author, year, url, etc.
        """
        # Create a unique key
        key = self._generate_key(entry)
        entry['ID'] = key
        self.entries.append(entry)
        return key

    def _generate_key(self, entry: Dict[str, Any]) -> str:
        """Generate firstauthorYear key."""
        authors = entry.get('author', ['Unknown'])
        if isinstance(authors, list):
            first_author = authors[0].split()[-1] # Last name
        else:
            first_author = str(authors).split()[-1]
            
        year = str(entry.get('year', '2026'))
        # Clean
        import re
        first_author = re.sub(r'[^a-zA-Z]', '', first_author)
        return f"{first_author}{year}"

    def generate_bibtex(self) -> str:
        """
        Generate the full .bib file content.
        Using bibtexparser or manual string formatting. Manual is often safer for simple needs.
        """
        bib_content = ""
        for e in self.entries:
            etype = e.get('entry_type', 'misc')
            key = e['ID']
            bib_content += f"@{etype}{{{key},\n"
            
            for field, value in e.items():
                if field in ['ID', 'entry_type']: continue
                if value:
                     # Escape tex special chars if needed, simplified here
                    bib_content += f"  {field} = {{{value}}},\n"
            
            bib_content += "}\n\n"
        return bib_content
