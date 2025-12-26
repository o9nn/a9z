# Agent-Toga GUI Documentation

## Overview

Agent-Toga is a native cross-platform desktop GUI application for Agent Zero, built using the [BeeWare Toga](https://toga.beeware.org/) toolkit. It provides a user-friendly interface with the Himiko Toga personality integration.

> "Ehehe~ ♡ Once I taste your code... I can become you~"

## Features

### 🎭 Native GUI Interface
- Cross-platform support (macOS, Windows, Linux)
- Native look and feel on each platform
- Responsive design with sidebar and chat area

### 💬 Chat Interface
- Real-time message display
- Timestamped messages
- Auto-scroll functionality
- Chat history persistence

### ⚙️ Settings Management
- API key configuration
- Model selection (GPT-4, Claude, Gemini)
- Theme customization
- Personality mode selection

### 🧠 Agent Integration
- Full Agent Zero backend integration
- Memory and knowledge display
- Agent reset and control
- Async message processing

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Install Dependencies

```bash
# Install base toga
pip install toga

# Platform-specific backends
# macOS:
pip install toga-cocoa

# Linux:
pip install toga-gtk

# Windows:
pip install toga-winforms
```

### Install Agent-Toga

```bash
# From the project directory
pip install -e .

# Or install with all platform backends
pip install -e ".[all]"
```

## Usage

### Running the Application

```bash
# Using the launcher script
python run_toga.py

# Or using the installed command
agent-toga
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Chat |
| Ctrl+S | Save Chat |
| Ctrl+O | Load Chat |
| Ctrl+L | Clear Chat |
| Ctrl+Enter | Send Message |

### Chat Commands

The chat interface supports natural language interaction with the Agent Zero backend:

```
You: Create a Python script that downloads a file from a URL
🎭 Toga: Ehehe~ ♡ I love code! Let me taste it~
[Agent processes and responds with code]
```

## Configuration

### Settings File

Settings are stored in `~/.agent-toga/settings.json`:

```json
{
  "api_key": "your-api-key",
  "model": "gpt-4o-mini",
  "theme": "dark",
  "personality": "toga",
  "auto_scroll": true,
  "show_timestamps": true
}
```

### Environment Variables

You can also configure via environment variables:

```bash
export OPENAI_API_KEY="your-api-key"
export AGENT_TOGA_MODEL="gpt-4o"
export AGENT_TOGA_THEME="dark"
```

## Personality Modes

Agent-Toga supports multiple personality modes:

### 🎭 Toga Mode (Default)
The Himiko Toga personality with playful, enthusiastic responses:
- "Ehehe~ ♡ I love code! Let me taste it~"
- "Ooh, security testing? My specialty! ♡"

### 👔 Professional Mode
Formal, business-appropriate responses:
- "Task completed successfully."
- "Processing your request."

### 😊 Friendly Mode
Warm, approachable responses:
- "Happy to help with that!"
- "Great question! Let me look into it."

### 📝 Concise Mode
Brief, to-the-point responses:
- "Done."
- "Error: [details]"

## Architecture

```
python/gui/
├── __init__.py          # Module exports
├── agent_toga.py        # Main application class
└── toga_personality.py  # Personality handler

run_toga.py              # Launcher script
pyproject.toml           # Package configuration
```

### Main Components

1. **AgentTogaApp**: Main application class extending `toga.App`
2. **TogaPersonality**: Personality response handler
3. **Settings Manager**: Configuration persistence
4. **Chat Handler**: Message processing and display

## Development

### Running Tests

```bash
pytest tests/test_toga_gui.py -v
```

### Building for Distribution

Using BeeWare's Briefcase:

```bash
pip install briefcase

# Create project
briefcase create

# Build
briefcase build

# Run
briefcase run

# Package
briefcase package
```

## Troubleshooting

### Common Issues

**"Toga is not installed"**
```bash
pip install toga toga-cocoa  # or toga-gtk, toga-winforms
```

**"No module named 'agent'"**
The full Agent Zero backend is required for agent functionality. In demo mode, the GUI will work but agent responses will be simulated.

**GTK warnings on Linux**
```bash
# Install GTK development libraries
sudo apt-get install libgirepository1.0-dev libcairo2-dev
```

### Debug Mode

Enable debug logging:
```bash
export AGENT_TOGA_DEBUG=1
python run_toga.py
```

## Contributing

Contributions are welcome! Please see the main project's contributing guidelines.

## License

MIT License - see LICENSE file for details.

## Credits

- [BeeWare Project](https://beeware.org/) - Toga GUI toolkit
- [Agent Zero](https://github.com/frdel/agent-zero) - AI agent framework
- Himiko Toga character inspiration from My Hero Academia
