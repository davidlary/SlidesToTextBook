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
        
        # Priority: SICE / Gemini Imagen (Excellence)
        # Priority: SICE / Gemini Imagen (Excellence)
        if self.client:
            try:
                from create_scientific_image import create_scientific_image
                
                # Scientific Diagram Prompt - High-End Upgrade (Project-Bastion Style)
                prompt = f"""Generate a stunning, high-end, publication-quality scientific visualization.
                DESCRIPTION: {figure_description}
                STYLE: Cinematic 3D Scientific Render. Unreal Engine 5 level detail. Octane Render. Glassmorphism.
                COMPOSITION: Clean, white background, professional typography, distinct color palette (corporate/scientific).
                REQUIREMENTS: No blurred text. No hand-drawn diagrams. Must look like a professional infographic or 3D render.
                """
                
                self.logger.info(f"Generating figure via SICE package: {filename}")
                # The package handles generation and validation
                img_path = create_scientific_image(
                    prompt, 
                    resolution=(1200, 800),
                    strict_mode=True,
                    return_metadata=False
                )
                
                if img_path:
                    # It returns a Path object directly now
                    from PIL import Image
                    if isinstance(img_path, Image.Image):
                        img_path.save(target_path)
                    else:
                        import shutil
                        from pathlib import Path
                        source = Path(img_path)
                        if source.exists():
                             shutil.copy(str(source), target_path)
                        else:
                             raise FileNotFoundError(f"Result path {source} does not exist.")
                    
                    self.logger.info(f"Generated figure via SICE: {target_path}")
                    return target_path

            except ImportError as e:
                self.logger.error(f"SICE package not found: {e}")
                raise RuntimeError("SICE package required for figure generation.") from e
            except Exception as e:
                self.logger.error(f"SICE generation failed: {e}")
                raise RuntimeError(f"SICE generation failed: {e}") from e
        
        return None

    def _generate_via_python(self, description: str, save_path: Path) -> bool:
        """Generate figure by writing and executing a Python script."""
        prompt = f"""
        Write a complete, standalone Python script using 'matplotlib' and 'seaborn' (if useful) to generate a **publication-quality** scientific figure.
        
        FIGURE CONCEPT: {description}
        OUTPUT FILE: "{save_path.absolute()}"
        
        REQUIREMENTS:
        1. Use 'matplotlib.pyplot'.
        2. **STYLE**: Use a professional, clean style (e.g., `plt.style.use('seaborn-v0_8-whitegrid')` or strictly classic with high-DPI settings).
        3. **COMPLEXITY**: The plot must be detailed (e.g., multiple curves, scatter with regression, 3D surface, or complex bar chart). Avoid simple single lines.
        4. **LABELS**: strictly label X and Y axes, include a Legend, and add meaningful Annotations pointing to key features.
        5. **COLOR**: Use a professional color palette (e.g., 'viridis', 'plasma', or 'Set2').
        6. Save the figure to the OUTPUT FILE path provided.
        7. Do NOT use plt.show().
        8. Aspect ratio should be 4:3 or 16:9.
        9. Font sizes should be legible (12+).
        
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
        
        # Determine style based on years
        is_historical = True
        if years and "19" in years:
             try:
                 start_year = int(years.split('-')[0].strip())
                 if start_year > 1900:
                     is_historical = False
             except:
                 pass

        try:
             # SICE Integration for Portraits
             from create_scientific_image import create_scientific_image
             
             style_desc = "classic, sepia-toned aesthetic, formal portrait style, soft vignette" if is_historical else "modern professional portrait, color, high quality"
             
             # Scientific Portrait Prompt - High-End Upgrade
             # Adaptive Logic: Switch to Landscape (4:3) for groups of 3+ people to prevent squishing.
             
             # Simple heuristic: count commas or 'and' to estimate group size
             approx_people = person_name.count(',') + person_name.count(' and ') + 1
             is_group = approx_people >= 3
             
             if is_group:
                 # LANDSCAPE STRATEGY (Groups > 2)
                 resolution = (1024, 768)
                 aspect_ratio_desc = "Horizontal (4:3)"
                 composition_desc = "Wide Cinematic Group Shot. All subjects visible side-by-side with equal prominence."
             else:
                 # PORTRAIT STRATEGY (Individuals or Pairs)
                 resolution = (768, 1024)
                 aspect_ratio_desc = "Vertical (3:4)"
                 composition_desc = "Extreme Close-up, head and shoulders only. Face must fill 85% of the frame. Minimal background."

             portrait_prompt = f"""Generate a high-end, publication-quality scientific image of {person_name}.
             DESCRIPTION: {person_name}
             COMPOSITION: {composition_desc} NO wasted whitespace.
             ASPECT RATIO: {aspect_ratio_desc}.
             STYLE: {style_desc}
             REQUIREMENTS: Photorealistic or Hyper-detailed oil painting style (depending on era). No text. No borders.
             """
             
             self.logger.info(f"Generating portrait via SICE package: {person_name} (Mode: {aspect_ratio_desc})")
             
             img_path = create_scientific_image(
                 portrait_prompt, 
                 resolution=resolution,
                 strict_mode=True,
                 return_metadata=False
             )
             
             if img_path:
                 # It returns a Path object directly now
                 from PIL import Image
                 
                 final_img = None
                 if isinstance(img_path, Image.Image):
                    final_img = img_path
                 else:
                    source = Path(img_path)
                    if source.exists():
                         final_img = Image.open(source)
                    else:
                         raise FileNotFoundError(f"Result path {source} does not exist.")
                 
                 # Save the correctly generated image directly.
                 # No cropping or resizing needed here as we requested the correct size.
                 if final_img:
                      final_img.save(target_path, quality=95)
                 
                 self.logger.info(f"Generated portrait via SICE: {target_path}")
                 return target_path
                 
        except ImportError:
             self.logger.error("SICE package not found.")
             raise RuntimeError("SICE package required for portrait generation.")
        except Exception as e:
            self.logger.error(f"Failed to generate portrait {filename}: {e}")
            raise RuntimeError(f"SICE portrait generation failed: {e}")
            
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
