import logging
import os
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
from slides_to_textbook.utils.image_clients import get_image_client

class FigureRecreator:
    def __init__(self, output_dir: Path):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = get_image_client()
        from slides_to_textbook.utils.api_clients import AIClient
        self.text_client = AIClient()

    def recreate_figure(self, figure_description: str, filename: str) -> Optional[Path]:
        """
        Generate a scientific figure. Tries Gemini/Imagen first, falls back to Matplotlib code.
        """
        target_path = self.output_dir / filename
        if target_path.exists():
            return target_path
            
        self.logger.info(f"Generating figure: {filename}")
        
        # Priority: Python Code for Scientific Diagrams (Excellence)
        if self._generate_via_python(figure_description, target_path):
            self.logger.info(f"Generated figure via Python: {target_path}")
            return target_path

        # Fallback to Image Gen
        if self.client:
             try:
                # Scientific Diagram Prompt
                prompt = f"""Generate a high-quality scientific diagram.
                DESCRIPTION: {figure_description}
                Clean, vector-like aesthetic, white background."""
                img = self.client.generate(prompt, resolution=(1200, 800))
                img.save(target_path)
                return target_path
             except Exception as e:
                self.logger.error(f"Image gen failed: {e}")
        
        return None

    def _generate_via_python(self, description: str, save_path: Path) -> bool:
        """Generate figure by writing and executing a Python script."""
        prompt = f"""
        Write a complete, standalone Python script using 'matplotlib' to generate a scientific figure.
        
        FIGURE DESCRIPTION: {description}
        OUTPUT FILE: "{save_path.absolute()}"
        
        REQUIREMENTS:
        1. Use 'matplotlib.pyplot'.
        2. Create high-quality, professional looking plot (use plt.style.use('ggplot') or similar standard style).
        3. Save the figure to the OUTPUT FILE path provided.
        4. Do NOT use plt.show().
        5. Aspect ratio should be 4:3.
        6. Font sizes should be legible (12+).
        
        Return ONLY the python code in a markdown block.
        """
        
        try:
            code_text = self.text_client.generate_text(prompt, system_prompt="You are a data visualization expert.", model="claude")
            
            # Extract code
            import re
            code_match = re.search(r'```python(.*?)```', code_text, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
                
                self.logger.info("Executing generated plotting code...")
                
                temp_script = save_path.with_suffix(".py.tmp")
                temp_script.write_text(code)
                
                import subprocess
                subprocess.check_call(["python", str(temp_script)])
                temp_script.unlink()
                
                if save_path.exists():
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"Python figure generation failed: {e}")
            return False

class PortraitGenerator:
    def __init__(self, output_dir: Path):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = get_image_client()

    def generate_portrait(self, person_name: str, years: str = "") -> Optional[Path]:
        """
        Generate a portrait using AI.
        """
        safe_name = person_name.replace(" ", "")
        filename = f"{safe_name}.jpg"
        target_path = self.output_dir / filename
        
        if target_path.exists():
            return target_path
            
        self.logger.info(f"Generating portrait for: {person_name}")
        
        if not self.client:
            self.logger.warning("No Image Client available. Skipping portrait.")
            return None

        # Determine style based on years
        is_historical = True
        if years and "19" in years:
             try:
                 start_year = int(years.split('-')[0].strip())
                 if start_year > 1900:
                     is_historical = False
             except:
                 pass

        style_prompt = "Sepia-toned aesthetic, formal portrait" if is_historical else "Modern professional portrait, color"
        prompt = f"Portrait of {person_name} ({years}). {style_prompt}. High quality, dignified."

        try:
             img = self.client.generate(prompt, resolution=(900, 1200))
             img.save(target_path)
             self.logger.info(f"Generated portrait saved to {target_path}")
             return target_path
        except Exception as e:
            self.logger.error(f"Failed to generate portrait {filename}: {e}")
            # Try Python Fallback (Silhouette)
            self.logger.info(f"Attempting Python Silhouette fallback for {person_name}")
            if self._generate_fallback_portrait_code(person_name, target_path, is_historical):
                return target_path
            return None

    def _generate_fallback_portrait_code(self, person_name: str, save_path: Path, is_historical: bool) -> bool:
        """Generate a stylized silhouette/placeholder using Matplotlib."""
        try:
            # We will generate a generic script.
            # In a real scenario, we could ask the LLM to write this, but for robustness/speed 
            # we can inject a known 'good enough' silhouette generator script or ask LLM for it.
            # Let's ask the LLM for a creative Matplotlib script.
            
            from slides_to_textbook.utils.api_clients import AIClient
            text_client = AIClient()
            
            style_desc = "classic, sepia-toned silhouette profile" if is_historical else "modern, clean abstract professional avatar"
            
            prompt = f"""
            Write a standalone Python script using 'matplotlib' to generate a artistic placeholder portrait for '{person_name}'.
            
            STYLE: {style_desc}
            OUTPUT FILE: "{save_path.absolute()}"
            
            REQUIREMENTS:
            1. Use 'matplotlib.pyplot'.
            2. The image should be artistic (e.g. valid abstract geometry, or a profile silhouette).
            3. It should NOT be a blank plot. Use shapes, text, or patterns.
            4. Include the person's name '{person_name}' artfully at the bottom.
            5. Save figure to OUTPUT FILE.
            6. No plt.show().
            7. IMPORTANT: Use ONLY valid standard matplotlib colormaps (e.g. 'copper', 'gray', 'Oranges', 'Blues'). DO NOT use 'Sepia'.
            
            Return ONLY the python code in a markdown block.
            """
            
            code_text = text_client.generate_text(prompt, system_prompt="You are a generative artist.", model="claude")
            
            import re
            import subprocess
            
            code_match = re.search(r'```python(.*?)```', code_text, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
                temp_script = save_path.with_suffix(".py.tmp")
                temp_script.write_text(code)
                subprocess.check_call(["python", str(temp_script)])
                temp_script.unlink()
                return save_path.exists()
                
            return False
            
        except Exception as e:
            self.logger.error(f"Silhouette fallback failed: {e}")
            return False
