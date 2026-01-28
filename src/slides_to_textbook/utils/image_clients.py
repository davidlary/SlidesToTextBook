"""
API clients for image generation, adapted from SICE package.

IMPORTANT: This module uses Google Gemini 2.0 Flash or Pro with specific prompting
strategies for high-quality scientific and historical image generation.
"""

import io
import time
import logging
import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from PIL import Image

# Setup logging
logger = logging.getLogger(__name__)

class ImageGenerationClient(ABC):
    """Abstract base class for image generation clients."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @abstractmethod
    def generate(
        self,
        prompt: str,
        resolution: tuple[int, int] = (1024, 1024),
        **kwargs
    ) -> Image.Image:
        """Generate image from prompt."""
        pass

class GeminiImageClient(ImageGenerationClient):
    """
    Google Gemini image generation client.
    Uses 'imagen-3.0-generate-002' (via google-genai) or available model.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key)
        try:
            import google.genai as genai
            from google.genai import types
            self.genai = genai
            self.types = types
            self.client = genai.Client(api_key=api_key)
            self.model_name = "imagen-3.0-generate-001" # Default to stable imagen
        except ImportError:
            raise ImportError(
                "google-genai package not installed. Install with: pip install google-genai"
            )

    def generate(
        self,
        prompt: str,
        resolution: tuple[int, int] = (1024, 1024),
        **kwargs
    ) -> Image.Image:
        """
        Generate image using Gemini/Imagen.
        """
        try:
            logger.info(f"Generating image with {self.model_name}...")
            
            # SICE Approach: Use generate_images
            response = self.client.models.generate_images(
                model=self.model_name,
                prompt=prompt,
                config=self.types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="3:4" if resolution[1] > resolution[0] else "4:3", # Approximate
                    # strict resolution matching is handled by post-resize
                )
            )

            if response.generated_images:
                image_bytes = response.generated_images[0].image.image_bytes
                image = Image.open(io.BytesIO(image_bytes))
                
                # Resize if needed to match exact specs
                if image.size != resolution:
                    image = image.resize(resolution, Image.Resampling.LANCZOS)
                    
                return image
            else:
                raise RuntimeError("No images returned in response")

        except Exception as e:
            logger.error(f"Gemini image generation failed: {e}")
            # Fallback or re-raise
            raise

def get_image_client() -> Optional[ImageGenerationClient]:
    """Factory to get configured image client."""
    key = os.getenv("GOOGLE_API_KEY")
    if key:
        return GeminiImageClient(key)
    return None
