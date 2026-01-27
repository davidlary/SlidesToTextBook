import logging
from typing import Dict, Any, List
from slides_to_textbook.utils.api_clients import AIClient

class ContentAuthor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ai_client = AIClient()

    def generate_chapter_content(self, topic_data: Dict[str, Any]) -> str:
        """
        Generate the full LaTeX content for a chapter based on topic data.
        """
        title = topic_data.get("title", "Untitled")
        self.logger.info(f"Generating content for chapter: {title}")
        
        # 1. Generate Intro/Context
        intro = self._generate_section("Introduction", topic_data, context="historical_context")
        
        # 2. Generate Main Sections
        sections_content = []
        for section_title in topic_data.get("sections", []):
            content = self._generate_section(section_title, topic_data)
            sections_content.append(content)
            
        # 3. Assemble
        # Note: The actual LaTeX wrapping (chapter, imports) happens in LaTeXBuilder.
        # This module produces the *body* content.
        
        full_content = f"\\section{{Introduction}}\n{intro}\n\n"
        full_content += "\n\n".join(sections_content)
        
        return full_content

    def _generate_section(self, section_title: str, topic_data: Dict[str, Any], context: str = "") -> str:
        """
        Generate text for a specific section.
        """
        system_prompt = """
        You are an expert textbook author. Write engaging, accessible, and mathematically precise content.
        Follow these rules:
        - Use LaTeX formatting for math ($...$ or $$...$$) and emphasis (\\textit{}, \\textbf{}).
        - Use \\citep{...} for citations (if you know them, otherwise leave a placeholder [CITATION]).
        - Do NOT include section headers (like \\section{...}) in the output, just the body text.
        - Tone: authoritative but inviting, similar to a high-quality academic textbook.
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
        Equations to include/explain: {', '.join(topic_data.get('equations', []))}
        
        Write approximately 500-800 words.
        """
        
        try:
            return self.ai_client.generate_text(prompt, system_prompt, model="claude")
        except Exception as e:
            self.logger.error(f"Failed to generate section {section_title}: {e}")
            return f"% Error generating section {section_title}"
