import logging
from typing import Dict, Any, List
from slides_to_textbook.utils.api_clients import AIClient

class ContentAuthor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ai_client = AIClient()

    def generate_chapter_content(self, topic_data: Dict[str, Any], assets_map: Dict[str, Any] = None, citation_map: Dict[str, str] = None) -> str:
        """
        Generate the full LaTeX content for a chapter based on topic data.
        """
        title = topic_data.get("title", "Untitled")
        self.logger.info(f"Generating content for chapter: {title}")
        
        # 1. Generate Intro/Context
        intro = self._generate_section("Introduction", topic_data, context="historical_context", assets_map=assets_map, citation_map=citation_map)
        
        # 2. Generate Main Sections
        sections_content = []
        for section_title in topic_data.get("sections", []):
            content = self._generate_section(section_title, topic_data, assets_map=assets_map, citation_map=citation_map)
            # Clean the content to remove duplicate headers and fix markdown
            content = self._clean_content(content, section_title)
            # WRAPPER FIX: Explicitly add the section header
            sections_content.append(f"\\section{{{section_title}}}\n{content}")
            
        full_content = f"\\section{{Introduction}}\n{intro}\n\n"
        full_content += "\n\n".join(sections_content)
        
        # 4. Deterministic Injection (The "Flawless" Guarantee)
        full_content = self._inject_missing_assets(full_content, assets_map)
        
        return full_content

    def _inject_missing_assets(self, content: str, assets_map: Dict[str, Any]) -> str:
        """
        Post-process content to ensure all relevant assets are included.
        If a concept/person is mentioned but the asset code is missing, append it.
        """
        if not assets_map: return content
        
        # 1. Figures
        for concept, filename in assets_map.get("figures", {}).items():
            # Check if concept is in text (case insensitive)
            if concept.lower() in content.lower():
                # Check if figure is already included
                if f"Figures/{filename}" not in content:
                    self.logger.info(f"Injecting missing figure for concept: {concept}")
                    # Simple injection: Append to the end of the section/text or near the first mention?
                    # Appending to the text block avoids breaking paragraphs.
                    # Ideally, we'd split paragraphs, but for robustness, let's append.
                    figure_code = f"\n\\begin{{figure}}[h]\n\\centering\n\\includegraphics[width=0.9\\linewidth]{{Figures/{filename}}}\n\\caption{{{concept}}}\n\\label{{fig:{concept.replace(' ', '')}}}\n\\end{{figure}}\n"
                    
                    # Try to insert after the paragraph containing the first mention
                    import re
                    # Split by double newline (paragraphs)
                    paragraphs = content.split("\n\n")
                    new_paragraphs = []
                    inserted = False
                    for p in paragraphs:
                        new_paragraphs.append(p)
                        if not inserted and concept.lower() in p.lower():
                            new_paragraphs.append(figure_code)
                            inserted = True
                    
                    if not inserted:
                        # Append to the end of the text if not inserted inline
                        # But typically we want it near the text. 
                        # Let's try to append to the last paragraph that contains the keyword, 
                        # or just append to end of section if logical.
                        # Simple robust fallback: Append to the end.
                        content += figure_code
                    else:
                        content = "\n\n".join(new_paragraphs)

        # 2. Portraits (Margin Notes)
        for person, filename in assets_map.get("portraits", {}).items():
             if person.lower() in content.lower():
                 # Check path using correct Portraits root
                 if f"Portraits/{filename}" not in content:
                     self.logger.info(f"Injecting missing portrait for: {person}")
                     note_code = f"\\automarginnote{{\\includegraphics[width=\\linewidth]{{Portraits/{filename}}}}}"
                     # Find first mention and replace name with Name + Note? 
                     # Or just insert unique note. Margin notes float, so placement matters less but should be close.
                     # Let's simple replace the first occurrence of the name with "Name\automarginnote{...}"
                     # But name might be part of a sentence.
                     
                     # Regex replace first occurrence ensuring word boundary
                     try:
                         pattern = re.compile(re.escape(person), re.IGNORECASE)
                         # Use lambda to avoid backslash escaping issues in the replacement string
                         content = pattern.sub(lambda m: f"{m.group(0)}{note_code}", content, count=1)
                     except Exception as e:
                         self.logger.error(f"Failed to inject portrait for {person}: {e}")

        return content

    def _generate_section(self, section_title: str, topic_data: Dict[str, Any], context: str = "", assets_map: Dict[str, Any] = None, citation_map: Dict[str, str] = None) -> str:
        """
        Generate text for a specific section.
        """
        assets_map = assets_map or {}
        citation_map = citation_map or {}
        
        # Format available assets for the prompt
        figures_info = "\n".join([f"- Concept '{k}': Use \\begin{{figure}}[h] \\centering \\includegraphics[width=0.9\\linewidth]{{Figures/{v}}} \\caption{{{k}}} \\label{{fig:{k.replace(' ', '')}}} \\end{{figure}}" for k, v in assets_map.get('figures', {}).items()])
        portraits_info = "\n".join([f"- Person '{k}': Use \\automarginnote{{\\includegraphics[width=\\linewidth]{{Portraits/{v}}} \\textbf{{{k}}}}}" for k, v in assets_map.get('portraits', {}).items()])
        citations_info = "\n".join([f"- {title}: use \\citep{{{key}}}" for title, key in citation_map.items()])

        system_prompt = """
        You are an expert textbook author. Write engaging, accessible, and mathematically precise content.
        Follow these rules:
        - Use LaTeX formatting for math ($...$ or $$...$$) and emphasis (\\textit{}, \\textbf{}).
        - **MANDATORY**: You MUST include the specific Figures and Margin Notes listed in the prompt if the text mentions the concept or person. 
        - **MANDATORY**: Use the specific Citation Keys provided. Do NOT invent citation keys.
        - Do NOT include section headers (like \\section{...}) in the output, just the body text.
        """
        
        topic_context = ""
        if context == "historical_context":
            topic_context = f"Historical Context: {topic_data.get('research', {}).get('historical_context', '')}"
            
        prompt = f"""
        Write the content for the section "{section_title}" of the chapter "{topic_data.get('title')}".
        
        Context/Background Info:
        {topic_data.get('description', '')}
        {topic_context}
        
        Key Concepts to cover: {', '.join(topic_data.get('concepts', []))}
        Key People: {', '.join(topic_data.get('people', []))}
        
        # REQUIRED ASSETS REMOVED TO PREVENT HALLUCINATIONS
        # We will inject them deterministically in post-processing.
        
        Use these Citations:
        {citations_info}
        
        Write an EXTREMELY DETAILED, COMPREHENSIVE textbook chapter section.
        Aim for at least 1500 words PER SECTION. 
        Deeply explain every concept with historical context, mathematical derivation, and practical examples.
        DO NOT SUMMARIZE. EXPAND on every detail.
        """
        
        try:
            return self.ai_client.generate_text(prompt, system_prompt, model="claude")
        except Exception as e:
            self.logger.error(f"Failed to generate section {section_title}: {e}")
            return f"% Error generating section {section_title}"

    def _clean_content(self, content: str, section_title: str) -> str:
        """
        Clean the raw AI output:
        1. Remove duplicate section headers at the start.
        2. Convert markdown bolding (**text**) to LaTeX (\\textbf{text}).
        """
        import re
        
        # 1. Remove duplicate header if strictly at the start
        # Check for "Section Title" or "\section{Section Title}" or "# Section Title"
        # Normalize: strip whitespace
        content = content.strip()
        
        # Simple check: does it start with the title?
        if content.lower().startswith(section_title.lower()):
            # Remove it (case insensitive match, but preserve case of rest)
            content = content[len(section_title):].strip()
            
        # Also check for repeated title on second line if first is empty
        lines = content.split('\n')
        if lines and lines[0].strip().lower() == section_title.lower():
             content = "\n".join(lines[1:]).strip()
             
        # 2. Fix Markdown Bold (**text**)
        # Regex: \*\*(.*?)\*\* -> \textbf{\1}
        # Non-greedy match for content inside asterisks
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        
        return content
