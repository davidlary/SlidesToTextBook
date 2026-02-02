import logging
import re
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

        # FIRST: Remove any AI-inserted portrait margin notes to avoid duplicates
        # Pattern: \automarginnote{\includegraphics[...]{Portraits/...}}
        portrait_pattern = r'\\automarginnote\{\\includegraphics\[width=\\linewidth\]\{Portraits/[^}]+\}\}'
        content = re.sub(portrait_pattern, '', content)
        self.logger.info("Stripped AI-inserted portrait margin notes to avoid duplicates")
        
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
                 # Check if portrait is already injected (filename already contains full path from OUTPUT_DIR)
                 if filename not in content:
                     self.logger.info(f"Injecting portrait for: {person}")
                     note_code = f"\\automarginnote{{\\includegraphics[width=\\linewidth]{{{filename}}}}}"
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
        # Note: assets_map paths are already relative to OUTPUT_DIR (e.g., "Portraits/Chapter-X/Name.png")
        figures_info = "\n".join([f"- Concept '{k}': Use \\begin{{figure}}[h] \\centering \\includegraphics[width=0.9\\linewidth]{{Figures/{v}}} \\caption{{{k}}} \\label{{fig:{k.replace(' ', '')}}} \\end{{figure}}" for k, v in assets_map.get('figures', {}).items()])
        portraits_info = "\n".join([f"- Person '{k}': Use \\automarginnote{{\\includegraphics[width=\\linewidth]{{{v}}}}}" for k, v in assets_map.get('portraits', {}).items()])
        citations_info = "\n".join([f"- {title}: use \\citep{{{key}}}" for title, key in citation_map.items()])

        system_prompt = """
        You are an expert textbook author writing in the style of the Air Quality V3 textbook.

        CRITICAL WRITING STYLE GUIDELINES:

        1. **Tone and Voice**:
           - Accessible yet authoritative - teach, don't lecture
           - Conversational transitions: "Now that we have...", "Let us turn our attention to..."
           - Engage the reader, don't present dry facts

        2. **Opening Sentences**:
           - Start with context or definition, NOT abstract concepts
           - Use patterns like "There is...", direct definitions
           - Establish relevance immediately

        3. **Concrete Details**:
           - MUST include specific examples with real places, dates, numbers
           - Quantitative details make concepts tangible
           - Example: "7-15 times the Mississippi" NOT "an order of magnitude"

        4. **Historical Context**:
           - Include etymology of key terms
           - Historical development of concepts
           - Cultural origins of terminology
           - Make history narrative and engaging

        5. **Technical Content**:
           - Define technical terms naturally in flowing text
           - Units always provided
           - Abbreviations defined on first use
           - Math integrated naturally, not prominently displayed

        6. **Paragraph Structure**:
           - Opening sentence establishes topic
           - Middle sentences develop with examples
           - Closing sentence connects to broader context
           - 4-8 sentences typical

        7. **Citations**:
           - Integrated smoothly using \\citep{key}
           - At end of sentence/clause
           - Common knowledge doesn't need citations

        8. **Cause-and-Effect**:
           - Clear causal chains step-by-step
           - Use "in turn" for cascading effects
           - Multi-step processes broken down

        9. **Real-World Connections**:
           - Constant connection to human impacts
           - Health implications
           - Environmental consequences
           - Practical applications

        10. **Active Voice**:
            - Prefer active over passive
            - Concrete verbs over abstract nouns
            - "Fog forms..." NOT "It is characterized by..."

        FORBIDDEN:
        - Do NOT start with abstract mathematics
        - Do NOT use dense academic prose
        - Do NOT overuse passive voice
        - Do NOT cite every sentence
        - Do NOT use jargon without explanation
        - Do NOT include section headers (like \\section{...}) in output
        - Do NOT add any \\automarginnote or \\includegraphics commands for portraits
        - Do NOT add meta-commentary like "Here is the content..."

        REQUIRED FORMAT:
        - Just write the textbook prose directly
        - Mention people by name in italics: \\textit{Name}
        - Portraits will be injected automatically
        - Use \\citep{key} for citations from the provided list
        - Use LaTeX formatting: $math$, \\textit{}, \\textbf{}
        """
        
        topic_context = ""
        if context == "historical_context":
            topic_context = f"Historical Context: {topic_data.get('research', {}).get('historical_context', '')}"
            
        prompt = f"""
        Write a comprehensive, engaging textbook section for "{section_title}" in the chapter "{topic_data.get('title')}".

        CONTEXT:
        {topic_data.get('description', '')}
        {topic_context}

        KEY CONCEPTS TO COVER: {', '.join(topic_data.get('concepts', []))}

        KEY PEOPLE TO MENTION: {', '.join(topic_data.get('people', []))}
        - Mention people naturally in the narrative using \\textit{{Name}}
        - Include their contributions and historical context
        - Portraits will be automatically added - you just write the text

        CITATIONS (use \\citep{{key}}):
        {citations_info}

        TARGET LENGTH: 1500+ words - write in depth with rich details

        WRITING APPROACH:
        - Start with an engaging opening that establishes context
        - Include etymology of key terms
        - Provide specific examples with places, dates, numbers
        - Explain historical development narratively
        - Show causal relationships step-by-step
        - Connect to real-world impacts (health, environment)
        - Use analogies for complex concepts
        - Write flowing paragraphs with natural transitions
        - Integrate citations smoothly at end of claims
        - Use active voice and concrete verbs

        Write the textbook prose directly below (no meta-commentary):
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
