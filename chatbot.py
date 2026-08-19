import os
from dotenv import load_dotenv
import google.generativeai as genai

class OSChatbot:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            print("WARNING: GEMINI_API_KEY is not set in .env properly.")
            
        genai.configure(api_key=self.api_key)
        self.model = None
        self.chat = None

    def initialize_with_prompt(self, prompt_filename):
        """Initializes the chat model with a specific system prompt."""
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY is missing. Please add it to the .env file.")

        system_prompt = "You are a helpful assistant."
        if prompt_filename:
            filepath = os.path.join("SYSTEM_PROMPTS", prompt_filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    system_prompt = f.read()
            except FileNotFoundError:
                print(f"WARNING: {filepath} not found. Using default prompt.")

        # Initialize the model with the system instruction
        self.model = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            system_instruction=system_prompt
        )
        
        # Start the chat session
        self.chat = self.model.start_chat()

    def send_message(self, message: str) -> str:
        """Sends a message to the model and returns the response."""
        if not self.chat:
            return "Error: Chatbot is not initialized with a prompt."
            
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini API: {str(e)}"
