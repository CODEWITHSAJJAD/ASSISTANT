# AI Assistant Project

A powerful and versatile AI assistant that combines voice recognition, text-to-speech, and real-time search capabilities with a modern graphical user interface.

## 🌟 Features

### Core Capabilities
- **Voice Recognition**: Interact with the assistant using voice commands
- **Text Input**: Type your queries directly into the interface
- **Text-to-Speech**: Get spoken responses from the assistant
- **Real-time Search**: Access up-to-date information from the web
- **Chat History**: Maintains conversation history for context
- **Modern GUI**: User-friendly interface built with CustomTkinter

### Advanced Features
- **Task Automation**: Control system functions and applications
- **Image Generation**: Create images based on text descriptions
- **Multi-threaded Operation**: Smooth performance with background processing
- **Customizable Assistant**: Personalize assistant name and user settings
- **Real-time Status Updates**: Visual feedback on assistant's current state

## 🛠️ Technical Stack

### Frontend
- CustomTkinter for modern UI
- PyQt5 for additional GUI components
- Edge-TTS for high-quality text-to-speech

### Backend
- Speech Recognition for voice input
- Real-time Search Engine for web queries
- Chatbot integration for natural conversations
- Image Generation capabilities
- System automation tools

## 📋 Prerequisites

- Python 3.x
- Required Python packages (listed in Requirements.txt)
- Internet connection for real-time features
- Microphone for voice input
- Speakers for voice output

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/CODEWITHSAJJAD/ASSISTANT
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r Requirements.txt
```

5. Create a `.env` file with your configuration:
```
USERNAME=YourName
ASSISTANTNAME=AssistantName
```

## 💻 Usage

1. Run the main application:
```bash
python Main.py
```

2. Interact with the assistant using either:
   - Voice commands (click the microphone button)
   - Text input (type in the input field)

3. The assistant can:
   - Answer general questions
   - Perform web searches
   - Generate images
   - Control system functions
   - Maintain conversation context

## 📁 Project Structure

```
├── Backend/
│   ├── Model.py
│   ├── RealtimeSearchEngine.py
│   ├── Automation.py
│   ├── Chatbot.py
│   ├── SpeechToText.py
│   ├── TextToSpeech.py
│   └── ImageGeneration.py
├── Frontend/
│   ├── GUI.py
│   └── Files/
├── Data/
│   └── ChatLog.json
├── Main.py
├── Requirements.txt
└── README.md
```

## 📚 File Descriptions

### Main Application Files
- **Main.py**: The core application file that orchestrates all components. It handles:
  - Initialization of the assistant
  - Voice and text input processing
  - Multi-threading for concurrent operations
  - Integration of all backend and frontend components
  - Chat history management
  - System automation triggers

### Backend Components
- **Model.py**: Contains the decision-making model that:
  - Processes user queries
  - Determines the type of response needed
  - Routes requests to appropriate handlers
  - Manages conversation flow

- **RealtimeSearchEngine.py**: Handles web-based queries:
  - Performs real-time web searches
  - Extracts relevant information
  - Formats search results
  - Integrates with various search APIs

- **Automation.py**: Manages system-level operations:
  - Application control (open/close)
  - System commands execution
  - Task automation
  - System resource management

- **Chatbot.py**: Implements conversational AI:
  - Natural language processing
  - Context-aware responses
  - Conversation history management
  - Response generation

- **SpeechToText.py**: Handles voice input:
  - Voice recognition
  - Audio processing
  - Speech-to-text conversion
  - Voice command interpretation

- **TextToSpeech.py**: Manages voice output:
  - Text-to-speech conversion
  - Voice synthesis
  - Audio playback
  - Voice customization

- **ImageGeneration.py**: Handles image creation:
  - Text-to-image conversion
  - Image generation from descriptions
  - Image processing and optimization
  - Image storage and retrieval

### Frontend Components
- **GUI.py**: Manages the user interface:
  - Modern UI implementation using CustomTkinter
  - User input handling
  - Display management
  - Status updates
  - Real-time feedback

- **Frontend/Files/**: Contains UI-related resources:
  - Temporary data storage
  - UI assets
  - Configuration files
  - Cache management

### Data Management
- **Data/ChatLog.json**: Stores conversation history:
  - User-assistant interactions
  - Timestamp tracking
  - Conversation context
  - Chat persistence

### Configuration
- **Requirements.txt**: Lists all project dependencies:
  - Python packages
  - Version specifications
  - Required libraries
  - External dependencies

## 🔧 Configuration

The assistant can be configured through the `.env` file:
- `USERNAME`: Your preferred name
- `ASSISTANTNAME`: Name for your AI assistant

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Known Issues

- Some features may require additional system permissions
- Internet connection is required for real-time features
- Voice recognition accuracy may vary based on environment

## 📞 Support

For support, please open an issue in the repository or contact the maintainers. 
