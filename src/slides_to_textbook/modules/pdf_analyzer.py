import logging
import json
import pdfplumber
import pytesseract
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image
from slides_to_textbook.utils.api_clients import AIClient

class PDFAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ai_client = AIClient()

    def analyze_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Main entry point: Extract content and analyze topics.
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        self.logger.info(f"Analyzing PDF: {path.name}")
        
        # 1. basic extraction
        raw_content = self.extract_content(path)
        
        # 2. structure analysis
        analysis = self._analyze_with_llm(raw_content)
        
        return {
            "file_name": path.name,
            "raw_content": raw_content,
            "analysis": analysis
        }

    def extract_content(self,  pdf_path: Path) -> Dict[str, Any]:
        """Extracts text and low-level objects from PDF."""
        pages_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                
                # Fallback to OCR if empty
                if not text.strip():
                    try:
                        # converting to image for OCR
                        # Convert to RGB to avoid PIL/Tesseract saving issues
                        im = page.to_image(resolution=300).original.convert("RGB")
                        text = pytesseract.image_to_string(im)
                    except Exception as e:
                        logging.warning(f"OCR failed for page {i+1}: {e}")
                        text = ""
                
                pages_content.append({
                    "page_number": i + 1,
                    "text": text,
                    # We could extract figures here too, but postponing complexity
                    # "figures": page.images # placeholder
                })
                
        return {"pages": pages_content}

    def _analyze_with_llm(self, raw_content: Dict[str, Any]) -> Dict[str, Any]:
        """Sends extracted text to LLM to identify topics/structure."""
        
        # Condense text for prompt
        full_text = "\n\n".join([f"Page {p['page_number']}:\n{p['text']}" for p in raw_content["pages"]])
        
        system_prompt = """
        You are an expert textbook author and curriculum designer. 
        Analyze the provided lecture slide content and extract a structured outline for a textbook chapter.
        Identify:
        1. Main Topic (Chapter Title)
        2. Key Concepts (Sections)
        3. Mathematical Equations (if any, describe them)
        4. Important Figures/People mentioned
        
        Output valid JSON only.
        """
        
        user_prompt = f"""
        Analyze the following lecture content and provide a JSON structure with:
        - "title": string
        - "description": string (brief summary)
        - "sections": list of strings (section headers)
        - "concepts": list of strings
        - "people": list of strings (names of historical figures)
        - "equations": list of strings (descriptions of math)

        Content:
        {full_text[:50000]} 
        """ 
        # Truncating to avoid massive context for now, though models handle large context.
        # 50k chars is safe for Sonnet.

        try:
            response_text = self.ai_client.generate_text(user_prompt, system_prompt, model="claude")
            # Cleanup json
            # Cleanup output to find valid JSON
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"LLM analysis failed: {e}")
            return {
                "title": "Unknown",
                "sections": [],
                "error": str(e)
            }
