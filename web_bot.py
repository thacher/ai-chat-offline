"""
AI Chat Offline - Web Interface
A Gradio-based web interface for the AI chatbot.
"""

import gradio as gr
import logging
from typing import List, Tuple
from bot import ChatbotConfig, Chatbot

# Configure logging for web interface
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global chatbot instance
chatbot_instance = None

def initialize_chatbot() -> bool:
    """Initialize the chatbot instance."""
    global chatbot_instance
    try:
        if chatbot_instance is None:
            config = ChatbotConfig()
            chatbot_instance = Chatbot(config)
            if not chatbot_instance.load_model():
                return False
        return True
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        return False

def chat_with_bot(message: str, history: List[dict]) -> Tuple[str, List[dict]]:
    """
    Handle chat interaction with the bot.
    
    Args:
        message: User's input message
        history: Chat history as list of message dictionaries
    
    Returns:
        Tuple of (empty string, updated history)
    """
    if not message or not message.strip():
        return "", history
    
    # Initialize chatbot if not already done
    if not initialize_chatbot():
        error_msg = "❌ Failed to initialize chatbot. Please check the logs."
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return "", history
    
    try:
        # Add user message to history
        history.append({"role": "user", "content": message})
        
        # Generate bot response
        response, success = chatbot_instance.generate_response(message)
        
        if success:
            # Add bot response to history
            history.append({"role": "assistant", "content": response})
        else:
            # Handle generation failure
            error_msg = "❌ Sorry, I encountered an error generating a response. Please try again."
            history.append({"role": "assistant", "content": error_msg})
        
        return "", history
    
    except Exception as e:
        logger.error(f"Error in chat_with_bot: {e}")
        error_msg = f"❌ An unexpected error occurred: {str(e)}"
        history.append({"role": "assistant", "content": error_msg})
        return "", history

def clear_chat() -> Tuple[str, List]:
    """Clear the chat history."""
    global chatbot_instance
    if chatbot_instance:
        chatbot_instance.chat_history_ids = None
        chatbot_instance.step_count = 0
    return "", []

def get_model_info() -> str:
    """Get information about the current AI core."""
    if chatbot_instance and chatbot_instance.config:
        config = chatbot_instance.config
        return f"""
**🤖 AI Core Diagnostics:**
- **🧠 Neural Network**: {config.model_name}
- **⚡ Processing Unit**: {config.device.upper()}
- **📏 Transmission Range**: {config.max_length} characters
- **🌡️ Creativity Level**: {config.temperature}
- **🎯 Focus Parameter**: {config.top_p}
- **🔄 Memory Cycles**: {config.max_conversation_steps}

**🛸 Space Station Status**: ✅ AI Core Online
        """
    return "🛸 **Space Station Status**: ⚠️ AI Core Not Initialized"

def create_interface():
    """Create and configure the Gradio interface."""
    
    # Modern Space Theme CSS
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important;
        min-height: 100vh !important;
        font-family: 'Space Mono', monospace !important;
    }
    
    /* Header Styling */
    .gradio-container h1 {
        background: linear-gradient(45deg, #00d4ff, #ff00ff, #00ff88) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5) !important;
    }
    
    /* Chat Interface */
    .chatbot {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Message Bubbles */
    .message {
        margin: 10px 0 !important;
        padding: 15px 20px !important;
        border-radius: 20px !important;
        max-width: 80% !important;
        word-wrap: break-word !important;
        position: relative !important;
    }
    
    .message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .message.assistant {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        color: white !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* Input Area */
    .textbox {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .textbox:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5) !important;
    }
    
    /* Buttons */
    .btn {
        background: linear-gradient(45deg, #00d4ff, #ff00ff) !important;
        border: none !important;
        border-radius: 25px !important;
        color: white !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    .btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5) !important;
    }
    
    .btn.secondary {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Panels */
    .panel {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        backdrop-filter: blur(10px) !important;
        margin: 10px 0 !important;
    }
    
    /* Status Indicator */
    .status {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px !important;
        color: #00ff88 !important;
        font-weight: bold !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00d4ff, #ff00ff) !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #ff00ff, #00d4ff) !important;
    }
    
    /* Animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 0 30px rgba(0, 212, 255, 0.6); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite !important;
    }
    
    .glowing {
        animation: glow 2s ease-in-out infinite !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 10px !important;
        }
        
        .message {
            max-width: 95% !important;
            padding: 12px 16px !important;
        }
    }
    """
    
    with gr.Blocks(css=css, title="AI Chat Offline", theme=gr.themes.Soft()) as interface:
        
        # Header with Space Theme
        gr.Markdown("""
        # 🚀 AI Chat Offline - Space Station
        
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 24px; margin-bottom: 10px;">🌌 Welcome to the AI Space Station 🌌</div>
            <div style="color: #00d4ff; font-size: 16px;">Your local AI chatbot running in deep space</div>
        </div>
        
        <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 15px; padding: 20px; margin: 20px 0;">
            <h3 style="color: #00d4ff; margin-top: 0;">🛸 Mission Features</h3>
            <ul style="color: white; margin: 0;">
                <li>🧠 <strong>Neural Network</strong> - Context-aware conversations</li>
                <li>💾 <strong>Memory Core</strong> - Automatic memory management</li>
                <li>🛡️ <strong>Shield Systems</strong> - Robust error handling</li>
                <li>🚀 <strong>Quantum Drive</strong> - GPU acceleration support</li>
                <li>🌌 <strong>Offline Mode</strong> - No internet required after setup</li>
            </ul>
        </div>
        """)
        
        # Chat interface
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="🌌 Communication Array",
                    height=500,
                    show_label=True,
                    container=True,
                    type="messages"
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="🛸 Transmit message to AI Space Station...",
                        label="📡 Transmission Input",
                        lines=2,
                        max_lines=4,
                        scale=4
                    )
                    send_btn = gr.Button("🚀 Launch Message", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("🧹 Clear Communication Log", variant="secondary")
                    info_btn = gr.Button("🔬 System Diagnostics", variant="secondary")
            
            with gr.Column(scale=1):
                # Model information panel
                model_info = gr.Markdown(
                    value="Click 'System Diagnostics' to load AI core information.",
                    label="🤖 AI Core Diagnostics"
                )
                
                # Status indicator
                status = gr.Markdown(
                    value="🟡 **Space Station Status**: Initializing AI Core...",
                    label="🛸 Station Status"
                )
                
                # Instructions
                gr.Markdown("""
                ### 🛸 Mission Protocol
                
                1. **🚀 First Launch**: AI Core will download automatically (~1-2 minutes)
                2. **📡 Communication**: Transmit your message and press Enter or click Launch
                3. **🧹 Reset**: Use "Clear Communication Log" to reset conversation history
                4. **🔬 Diagnostics**: Click "System Diagnostics" to see AI core details
                
                ### ⚠️ Space Station Notes
                - AI Core downloads only on first use
                - Communication history resets after 10 exchanges
                - Check terminal for detailed mission logs
                - Quantum entanglement requires stable connection
                """)
        
        # Event handlers
        def send_message(message, history):
            return chat_with_bot(message, history)
        
        def update_status():
            if chatbot_instance and chatbot_instance.model:
                return "🟢 **Space Station Status**: AI Core Online - Ready for Communication!"
            else:
                return "🟡 **Space Station Status**: Initializing AI Core..."
        
        # Connect events
        msg_input.submit(send_message, [msg_input, chatbot], [msg_input, chatbot])
        send_btn.click(send_message, [msg_input, chatbot], [msg_input, chatbot])
        clear_btn.click(clear_chat, outputs=[msg_input, chatbot])
        info_btn.click(get_model_info, outputs=model_info)
        
        # Auto-update status
        interface.load(update_status, outputs=status)
    
    return interface

def main():
    """Main function to launch the web interface."""
    try:
        print("🚀 Launching AI Space Station Web Interface...")
        print("🌌 Opening Space Station Control Panel in your browser")
        print("🛸 Space Station URL: http://localhost:3000")
        print("⏳ AI Core initialization may take 1-2 minutes on first launch")
        print("=" * 60)
        
        # Create and launch interface
        interface = create_interface()
        
        # Launch with specific settings
        interface.launch(
            server_name="127.0.0.1",  # Local only
            server_port=3000,         # Standard web dev port
            share=False,             # Don't create public link
            debug=False,             # Disable debug mode
            show_error=True,         # Show errors in interface
            quiet=False              # Show startup messages
        )
        
    except Exception as e:
        logger.error(f"Failed to launch web interface: {e}")
        print(f"❌ Error launching web interface: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
