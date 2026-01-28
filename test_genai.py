
import os
import logging
from google.genai import Client, types
from PIL import Image
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestGenAI")

def test_genai():
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        logger.error("GOOGLE_API_KEY not set")
        return

    client = Client(api_key=key)
    logger.info("Client created.")

    prompt = "A small red apple."
    try:
        logger.info(f"Generating: {prompt}")
        response = client.models.generate_images(
            model="imagen-3.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        if response.generated_images:
            logger.info("Success! Image generated.")
            image_bytes = response.generated_images[0].image.image_bytes
            logger.info(f"Bytes received: {len(image_bytes)}")
        else:
            logger.error("No images returned.")
    except Exception as e:
        logger.error(f"Generation failed: {e}")

if __name__ == "__main__":
    test_genai()
