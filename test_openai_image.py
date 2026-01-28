
import os
import logging
from openai import OpenAI
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestOpenAI")

def test_openai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        logger.error("OPENAI_API_KEY not set")
        return

    client = OpenAI(api_key=key)
    logger.info("Client created.")

    prompt = "A small red apple, high quality."
    try:
        logger.info(f"Generating: {prompt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        url = response.data[0].url
        logger.info(f"Success! Image URL: {url}")
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")

if __name__ == "__main__":
    test_openai()
