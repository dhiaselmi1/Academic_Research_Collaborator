import google.generativeai as genai
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import os

# Hardcoded API key (replace with your actual key)
GEMINI_API_KEY = "AIzaSyCF6MydBh6Kacv_14cNoZimz7A0oq6iPOs"


class BaseAgent(ABC):
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.memory_path = "../../memory/memory_store.json"

    def load_memory(self) -> Dict[str, Any]:
        """Load memory from JSON file"""
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "research_question": "",
                "citations": [],
                "notes": [],
                "literature_reviews": [],
                "hypotheses": [],
                "drafts": [],
                "progress": {
                    "literature_review_completed": False,
                    "hypothesis_validated": False,
                    "draft_polished": False
                }
            }

    def save_memory(self, memory: Dict[str, Any]) -> None:
        """Save memory to JSON file"""
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(memory, f, indent=2, ensure_ascii=False)

    def generate_response(self, prompt: str) -> str:
        """Generate response using Gemini Flash 2.0"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass

    def update_memory(self, key: str, value: Any) -> None:
        """Update specific memory key"""
        memory = self.load_memory()
        if key in memory:
            if isinstance(memory[key], list):
                memory[key].append(value)
            else:
                memory[key] = value
        else:
            memory[key] = value
        self.save_memory(memory)