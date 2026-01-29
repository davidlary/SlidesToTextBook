import os
import logging
import anthropic
from typing import Optional, Dict, Any, List

class AIClient:
    def __init__(self):
        self.anthropic_client = None
        self.gemini_client = None
        self.gemini_configured = False
        self._setup_clients()

    def _setup_clients(self):
        # Setup Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        
        # Setup Gemini (New SDK)
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=google_key)
                self.gemini_configured = True
            except ImportError:
                logging.warning("google-genai not installed. Gemini unavailable.")

    def generate_text(self, prompt: str, system_prompt: str = "", model: str = "claude") -> str:
        """
        Generate text using specified model.
        model: 'claude' (default) or 'gemini'
        """
        # Default to Claude if verified working
        if model == "claude" and self.anthropic_client:
            return self._call_claude(prompt, system_prompt)
        elif model == "gemini" and self.gemini_configured:
            return self._call_gemini(prompt, system_prompt)
        else:
            # Fallback
            if self.anthropic_client:
                return self._call_claude(prompt, system_prompt)
            elif self.gemini_configured:
                return self._call_gemini(prompt, system_prompt)
            else:
                raise RuntimeError("No AI clients configured (missing API keys)")

    def _call_claude(self, prompt: str, system_prompt: str) -> str:
        if not self.anthropic_client: raise ValueError("Client not set")
        message = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4096,
            temperature=0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def _call_gemini(self, prompt: str, system_prompt: str) -> str:
        if not self.gemini_configured: raise ValueError("Gemini not configured")
        
        response = self.gemini_client.models.generate_content(
            model='gemini-2.0-flash-exp', 
            contents=prompt,
            config={'system_instruction': system_prompt}
        )
        return response.text
