import os
import anthropic
import google.generativeai as genai
from typing import Optional, Dict, Any, List

class AIClient:
    def __init__(self):
        self.anthropic_client = None
        self.gemini_configured = False
        self._setup_clients()

    def _setup_clients(self):
        # Setup Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        
        # Setup Gemini
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            genai.configure(api_key=google_key)
            self.gemini_configured = True

    def generate_text(self, prompt: str, system_prompt: str = "", model: str = "claude") -> str:
        """
        Generate text using specified model.
        model: 'claude' (default) or 'gemini'
        """
        if model == "claude" and self.anthropic_client:
            return self._call_claude(prompt, system_prompt)
        elif model == "gemini" and self.gemini_configured:
            return self._call_gemini(prompt, system_prompt)
        else:
            # Fallback logic or error
            if self.anthropic_client:
                return self._call_claude(prompt, system_prompt)
            elif self.gemini_configured:
                return self._call_gemini(prompt, system_prompt)
            else:
                raise RuntimeError("No AI clients configured (missing API keys)")

    def _call_claude(self, prompt: str, system_prompt: str) -> str:
        message = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229", # Or latest available
            max_tokens=4096,
            temperature=0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def _call_gemini(self, prompt: str, system_prompt: str) -> str:
        # Gemini doesn't have system prompt exactly same way in older versions, 
        # but 1.5 pro does. We'll prepend system prompt.
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
