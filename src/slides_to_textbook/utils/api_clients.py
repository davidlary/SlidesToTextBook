import os
import logging
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
            try:
                return self._call_claude(prompt, system_prompt)
            except Exception as e:
                logging.warning(f"Claude call failed: {e}. Falling back to mock.")
                return self._mock_response(prompt)
        elif model == "gemini" and self.gemini_configured:
            try:
                return self._call_gemini(prompt, system_prompt)
            except Exception as e:
                logging.warning(f"Gemini call failed: {e}. Falling back to mock.")
                return self._mock_response(prompt)
        else:
             logging.warning("No AI client available. Using mock response.")
             return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        """Return structured mock data based on prompt context."""
        if "JSON" in prompt or "json" in prompt:
            return '''
            {
                "title": "Introduction to Machine Learning",
                "description": "An overview of ML concepts.",
                "sections": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"],
                "concepts": ["Training Data", "Model", "Loss Function"],
                "people": ["Arthur Samuel", "Alan Turing"],
                "equations": ["y = f(x)", "L(w)"]
            }
            '''
        else:
            return "This is a placeholder content generated because the AI API keys were missing or invalid. " \
                   "It follows the structure requested but lacks real generated prose. " \
                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

    def _call_claude(self, prompt: str, system_prompt: str) -> str:
        if not self.anthropic_client: raise ValueError("Client not set")
        message = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
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
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
