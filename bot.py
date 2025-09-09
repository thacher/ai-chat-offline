"""
AI Chat Offline - A local chatbot using Hugging Face's DialoGPT model.

This module provides an interactive chatbot that runs locally without requiring
internet connectivity after the initial model download.
"""

import logging
import sys
from typing import Optional, Tuple
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ChatbotConfig:
    """Configuration class for chatbot parameters."""
    
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.max_length = 1000
        self.temperature = 0.7
        self.top_p = 0.9
        self.max_conversation_steps = 10
        self.device = "cuda" if torch.cuda.is_available() else "cpu"


class Chatbot:
    """Main chatbot class handling conversation logic."""
    
    def __init__(self, config: ChatbotConfig):
        self.config = config
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForCausalLM] = None
        self.chat_history_ids: Optional[torch.Tensor] = None
        self.step_count = 0
        
    def load_model(self) -> bool:
        """Load the tokenizer and model with error handling."""
        try:
            logger.info(f"Loading model: {self.config.model_name}")
            logger.info(f"Using device: {self.config.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if self.config.device == "cuda" else torch.float32
            )
            
            # Move model to device
            self.model.to(self.config.device)
            
            logger.info("Model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def validate_input(self, user_input: str) -> bool:
        """Validate user input."""
        if not user_input or not user_input.strip():
            return False
        return True
    
    def generate_response(self, user_input: str) -> Tuple[str, bool]:
        """Generate bot response with error handling."""
        try:
            if not self.validate_input(user_input):
                return "Please provide a valid input.", False
            
            # Encode user input
            new_input_ids = self.tokenizer.encode(
                user_input + self.tokenizer.eos_token, 
                return_tensors="pt"
            ).to(self.config.device)
            
            # Concatenate with chat history if it exists
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1)
            else:
                bot_input_ids = new_input_ids
            
            # Generate response
            with torch.no_grad():
                self.chat_history_ids = self.model.generate(
                    bot_input_ids,
                    max_length=self.config.max_length,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    num_return_sequences=1,
                    early_stopping=True
                )
            
            # Decode response
            bot_response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
                skip_special_tokens=True
            ).strip()
            
            self.step_count += 1
            
            # Reset conversation if needed
            if self.step_count >= self.config.max_conversation_steps:
                logger.info("Resetting conversation history to prevent memory overflow")
                self.chat_history_ids = None
                self.step_count = 0
            
            return bot_response, True
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error. Please try again.", False
    
    def run(self) -> None:
        """Main conversation loop."""
        if not self.load_model():
            logger.error("Failed to load model. Exiting.")
            return
        
        print("🤖 AI Chatbot is ready! Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Check for exit conditions
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                
                # Generate and display response
                response, success = self.generate_response(user_input)
                print(f"🤖 Bot: {response}")
                
                if not success:
                    print("⚠️  There was an issue with the response generation.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {str(e)}")
                print("❌ An unexpected error occurred. Please try again.")


def main():
    """Main entry point for the chatbot application."""
    try:
        config = ChatbotConfig()
        chatbot = Chatbot(config)
        chatbot.run()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
