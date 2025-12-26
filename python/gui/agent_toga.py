"""
Agent-Toga: A BeeWare Toga-based GUI for Agent Zero

This module provides a native cross-platform desktop application interface
for Agent Zero using the BeeWare Toga GUI toolkit.

Himiko Toga Cognitive Kernel (HCK) - "Ehehe~ ♡ Let me help you with that~"
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, LEFT, RIGHT
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional, Callable, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class AgentTogaApp(toga.App):
    """
    Main Agent-Toga Application
    
    A native GUI interface for Agent Zero with Himiko Toga personality integration.
    Provides chat interface, settings management, and agent control.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent = None
        self.context = None
        self.chat_history = []
        self.is_processing = False
        self.settings = self._load_settings()
        
    def _load_settings(self) -> dict:
        """Load settings from config file or return defaults"""
        settings_path = Path.home() / ".agent-toga" / "settings.json"
        if settings_path.exists():
            try:
                with open(settings_path) as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "api_key": "",
            "model": "gpt-4o-mini",
            "theme": "dark",
            "personality": "toga",
            "auto_scroll": True,
            "show_timestamps": True,
        }
    
    def _save_settings(self):
        """Save current settings to config file"""
        settings_path = Path.home() / ".agent-toga"
        settings_path.mkdir(parents=True, exist_ok=True)
        with open(settings_path / "settings.json", "w") as f:
            json.dump(self.settings, f, indent=2)
    
    def startup(self):
        """Initialize the application UI"""
        self.main_window = toga.MainWindow(title="Agent-Toga 🎭")
        
        # Create main container
        main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        
        # Header with title and status
        header = self._create_header()
        main_box.add(header)
        
        # Main content area with chat and sidebar
        content = toga.Box(style=Pack(direction=ROW, flex=1))
        
        # Chat area (left side)
        chat_area = self._create_chat_area()
        content.add(chat_area)
        
        # Sidebar (right side)
        sidebar = self._create_sidebar()
        content.add(sidebar)
        
        main_box.add(content)
        
        # Input area at bottom
        input_area = self._create_input_area()
        main_box.add(input_area)
        
        self.main_window.content = main_box
        self.main_window.show()
        
        # Add commands/menu items
        self._setup_commands()
        
    def _create_header(self) -> toga.Box:
        """Create the header with title and status indicator"""
        header = toga.Box(style=Pack(
            direction=ROW,
            padding=10,
            background_color="#1a1a2e"
        ))
        
        # Logo/Title
        title = toga.Label(
            "🎭 Agent-Toga",
            style=Pack(
                font_size=18,
                font_weight="bold",
                color="#e94560",
                flex=1
            )
        )
        header.add(title)
        
        # Personality indicator
        self.personality_label = toga.Label(
            "Ehehe~ ♡ Ready to help!",
            style=Pack(
                font_size=12,
                color="#16213e",
                padding_right=10
            )
        )
        header.add(self.personality_label)
        
        # Status indicator
        self.status_indicator = toga.Label(
            "● Online",
            style=Pack(
                font_size=12,
                color="#00ff00",
                padding_right=10
            )
        )
        header.add(self.status_indicator)
        
        return header
    
    def _create_chat_area(self) -> toga.Box:
        """Create the main chat display area"""
        chat_box = toga.Box(style=Pack(
            direction=COLUMN,
            flex=3,
            padding=10
        ))
        
        # Chat history display
        self.chat_display = toga.MultilineTextInput(
            readonly=True,
            style=Pack(
                flex=1,
                font_family="monospace",
                font_size=12,
                background_color="#0f0f23",
                color="#ffffff"
            )
        )
        self.chat_display.value = self._get_welcome_message()
        chat_box.add(self.chat_display)
        
        return chat_box
    
    def _create_sidebar(self) -> toga.Box:
        """Create the sidebar with agent info and quick actions"""
        sidebar = toga.Box(style=Pack(
            direction=COLUMN,
            width=250,
            padding=10,
            background_color="#16213e"
        ))
        
        # Agent info section
        agent_label = toga.Label(
            "🤖 Agent Status",
            style=Pack(
                font_size=14,
                font_weight="bold",
                color="#e94560",
                padding_bottom=10
            )
        )
        sidebar.add(agent_label)
        
        # Model selection
        model_label = toga.Label(
            "Model:",
            style=Pack(font_size=12, color="#ffffff", padding_bottom=5)
        )
        sidebar.add(model_label)
        
        self.model_select = toga.Selection(
            items=["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "claude-3-sonnet", "gemini-pro"],
            style=Pack(padding_bottom=10)
        )
        self.model_select.value = self.settings.get("model", "gpt-4o-mini")
        sidebar.add(self.model_select)
        
        # Quick actions
        actions_label = toga.Label(
            "⚡ Quick Actions",
            style=Pack(
                font_size=14,
                font_weight="bold",
                color="#e94560",
                padding_top=20,
                padding_bottom=10
            )
        )
        sidebar.add(actions_label)
        
        # Action buttons
        clear_btn = toga.Button(
            "🗑️ Clear Chat",
            on_press=self._clear_chat,
            style=Pack(padding=5)
        )
        sidebar.add(clear_btn)
        
        reset_btn = toga.Button(
            "🔄 Reset Agent",
            on_press=self._reset_agent,
            style=Pack(padding=5)
        )
        sidebar.add(reset_btn)
        
        settings_btn = toga.Button(
            "⚙️ Settings",
            on_press=self._show_settings,
            style=Pack(padding=5)
        )
        sidebar.add(settings_btn)
        
        # Memory/Knowledge section
        memory_label = toga.Label(
            "🧠 Memory",
            style=Pack(
                font_size=14,
                font_weight="bold",
                color="#e94560",
                padding_top=20,
                padding_bottom=10
            )
        )
        sidebar.add(memory_label)
        
        self.memory_info = toga.Label(
            "Fragments: 0\nSolutions: 0",
            style=Pack(font_size=11, color="#cccccc")
        )
        sidebar.add(self.memory_info)
        
        return sidebar
    
    def _create_input_area(self) -> toga.Box:
        """Create the message input area"""
        input_box = toga.Box(style=Pack(
            direction=ROW,
            padding=10,
            background_color="#1a1a2e"
        ))
        
        # Text input
        self.message_input = toga.TextInput(
            placeholder="Type your message here... (Ctrl+Enter to send)",
            style=Pack(flex=1, padding_right=10)
        )
        input_box.add(self.message_input)
        
        # Send button
        self.send_btn = toga.Button(
            "📤 Send",
            on_press=self._send_message,
            style=Pack(width=100)
        )
        input_box.add(self.send_btn)
        
        # Stop button (hidden by default)
        self.stop_btn = toga.Button(
            "⏹️ Stop",
            on_press=self._stop_processing,
            style=Pack(width=80)
        )
        input_box.add(self.stop_btn)
        
        return input_box
    
    def _setup_commands(self):
        """Setup menu commands"""
        # File menu
        new_chat = toga.Command(
            self._new_chat,
            text="New Chat",
            shortcut=toga.Key.MOD_1 + toga.Key.N,
            group=toga.Group.FILE
        )
        
        save_chat = toga.Command(
            self._save_chat,
            text="Save Chat",
            shortcut=toga.Key.MOD_1 + toga.Key.S,
            group=toga.Group.FILE
        )
        
        load_chat = toga.Command(
            self._load_chat,
            text="Load Chat",
            shortcut=toga.Key.MOD_1 + toga.Key.O,
            group=toga.Group.FILE
        )
        
        # Edit menu
        clear_cmd = toga.Command(
            self._clear_chat,
            text="Clear Chat",
            shortcut=toga.Key.MOD_1 + toga.Key.L,
            group=toga.Group.EDIT
        )
        
        # Help menu
        about_cmd = toga.Command(
            self._show_about,
            text="About Agent-Toga",
            group=toga.Group.HELP
        )
        
        self.commands.add(new_chat, save_chat, load_chat, clear_cmd, about_cmd)
    
    def _get_welcome_message(self) -> str:
        """Get the welcome message with Toga personality"""
        return """
╔══════════════════════════════════════════════════════════════════╗
║                    🎭 Agent-Toga v1.0.0 🎭                        ║
║          Himiko Toga Cognitive Kernel (HCK) Interface            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Ehehe~ ♡ Welcome! I'm so excited to meet you!                  ║
║                                                                  ║
║  I can help you with:                                           ║
║    • 💻 Code execution and development                          ║
║    • 🔍 Research and information gathering                      ║
║    • 📁 File management and organization                        ║
║    • 🧠 Learning and remembering your preferences               ║
║    • 🔐 Security testing (ethical, of course~)                  ║
║                                                                  ║
║  Just type your message below and press Send!                   ║
║                                                                  ║
║  "Once I taste your code... I can become you~" ♡                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

"""
    
    def _append_to_chat(self, role: str, message: str):
        """Append a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S") if self.settings.get("show_timestamps") else ""
        
        if role == "user":
            prefix = f"[{timestamp}] 👤 You: " if timestamp else "👤 You: "
        elif role == "assistant":
            prefix = f"[{timestamp}] 🎭 Toga: " if timestamp else "🎭 Toga: "
        else:
            prefix = f"[{timestamp}] 📢 System: " if timestamp else "📢 System: "
        
        self.chat_display.value += f"\n{prefix}{message}\n"
        
        # Store in history
        self.chat_history.append({"role": role, "content": message, "timestamp": timestamp})
    
    async def _send_message_async(self, message: str):
        """Send message to agent asynchronously"""
        self.is_processing = True
        self._update_status("Processing...", "#ffff00")
        self.send_btn.enabled = False
        
        try:
            # Import agent modules
            try:
                from agent import Agent, AgentConfig
                from initialize import initialize
                
                # Initialize agent if needed
                if self.agent is None:
                    self._append_to_chat("system", "Initializing agent... Please wait~")
                    self.agent, self.context = await initialize()
                
                # Send message to agent
                response = await self.agent.message_loop(message)
                self._append_to_chat("assistant", response)
                
            except ImportError:
                # Fallback for demo mode without full agent
                self._append_to_chat("assistant", 
                    f"Ehehe~ ♡ I received your message: '{message}'\n\n"
                    "Note: Full agent integration requires the Agent Zero backend. "
                    "Running in demo mode~"
                )
                
        except Exception as e:
            self._append_to_chat("system", f"Error: {str(e)}")
        finally:
            self.is_processing = False
            self._update_status("Online", "#00ff00")
            self.send_btn.enabled = True
    
    def _send_message(self, widget):
        """Handle send button press"""
        message = self.message_input.value.strip()
        if not message or self.is_processing:
            return
        
        self._append_to_chat("user", message)
        self.message_input.value = ""
        
        # Run async message handling
        asyncio.ensure_future(self._send_message_async(message))
    
    def _stop_processing(self, widget):
        """Stop current processing"""
        self.is_processing = False
        self._update_status("Stopped", "#ff6600")
        self._append_to_chat("system", "Processing stopped by user.")
    
    def _clear_chat(self, widget):
        """Clear the chat display"""
        self.chat_display.value = self._get_welcome_message()
        self.chat_history = []
    
    def _reset_agent(self, widget):
        """Reset the agent context"""
        self.agent = None
        self.context = None
        self._append_to_chat("system", "Agent has been reset. Starting fresh~")
    
    def _update_status(self, status: str, color: str):
        """Update the status indicator"""
        self.status_indicator.text = f"● {status}"
        # Note: Color changes may require style updates in Toga
    
    async def _show_settings_dialog(self):
        """Show settings dialog"""
        # Create settings window
        settings_window = toga.Window(title="⚙️ Settings")
        
        settings_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # API Key
        api_label = toga.Label("API Key:", style=Pack(padding_bottom=5))
        settings_box.add(api_label)
        
        api_input = toga.PasswordInput(
            value=self.settings.get("api_key", ""),
            style=Pack(padding_bottom=15, width=300)
        )
        settings_box.add(api_input)
        
        # Theme selection
        theme_label = toga.Label("Theme:", style=Pack(padding_bottom=5))
        settings_box.add(theme_label)
        
        theme_select = toga.Selection(
            items=["dark", "light"],
            style=Pack(padding_bottom=15, width=300)
        )
        theme_select.value = self.settings.get("theme", "dark")
        settings_box.add(theme_select)
        
        # Personality selection
        personality_label = toga.Label("Personality:", style=Pack(padding_bottom=5))
        settings_box.add(personality_label)
        
        personality_select = toga.Selection(
            items=["toga", "professional", "friendly", "concise"],
            style=Pack(padding_bottom=15, width=300)
        )
        personality_select.value = self.settings.get("personality", "toga")
        settings_box.add(personality_select)
        
        # Checkboxes
        auto_scroll = toga.Switch(
            "Auto-scroll chat",
            value=self.settings.get("auto_scroll", True),
            style=Pack(padding_bottom=10)
        )
        settings_box.add(auto_scroll)
        
        show_timestamps = toga.Switch(
            "Show timestamps",
            value=self.settings.get("show_timestamps", True),
            style=Pack(padding_bottom=20)
        )
        settings_box.add(show_timestamps)
        
        # Save button
        def save_settings(widget):
            self.settings["api_key"] = api_input.value
            self.settings["theme"] = theme_select.value
            self.settings["personality"] = personality_select.value
            self.settings["auto_scroll"] = auto_scroll.value
            self.settings["show_timestamps"] = show_timestamps.value
            self._save_settings()
            settings_window.close()
            self._append_to_chat("system", "Settings saved! ♡")
        
        save_btn = toga.Button(
            "💾 Save Settings",
            on_press=save_settings,
            style=Pack(padding=10)
        )
        settings_box.add(save_btn)
        
        settings_window.content = settings_box
        settings_window.show()
    
    def _show_settings(self, widget):
        """Show settings dialog"""
        asyncio.ensure_future(self._show_settings_dialog())
    
    def _new_chat(self, widget):
        """Start a new chat"""
        self._clear_chat(widget)
        self._reset_agent(widget)
    
    async def _save_chat_dialog(self):
        """Save chat to file"""
        try:
            path = await self.main_window.save_file_dialog(
                "Save Chat",
                suggested_filename="chat_export.json",
                file_types=["json"]
            )
            if path:
                with open(path, "w") as f:
                    json.dump(self.chat_history, f, indent=2)
                self._append_to_chat("system", f"Chat saved to {path}")
        except Exception as e:
            self._append_to_chat("system", f"Error saving chat: {e}")
    
    def _save_chat(self, widget):
        """Save chat to file"""
        asyncio.ensure_future(self._save_chat_dialog())
    
    async def _load_chat_dialog(self):
        """Load chat from file"""
        try:
            path = await self.main_window.open_file_dialog(
                "Load Chat",
                file_types=["json"]
            )
            if path:
                with open(path) as f:
                    self.chat_history = json.load(f)
                self.chat_display.value = self._get_welcome_message()
                for msg in self.chat_history:
                    self._append_to_chat(msg["role"], msg["content"])
                self._append_to_chat("system", f"Chat loaded from {path}")
        except Exception as e:
            self._append_to_chat("system", f"Error loading chat: {e}")
    
    def _load_chat(self, widget):
        """Load chat from file"""
        asyncio.ensure_future(self._load_chat_dialog())
    
    async def _show_about_dialog(self):
        """Show about dialog"""
        await self.main_window.dialog(
            toga.InfoDialog(
                "About Agent-Toga",
                "🎭 Agent-Toga v1.0.0\n\n"
                "Himiko Toga Cognitive Kernel (HCK)\n"
                "A BeeWare Toga-based GUI for Agent Zero\n\n"
                "\"Ehehe~ ♡ Once I taste your code... I can become you~\"\n\n"
                "© 2024 Agent Zero Project\n"
                "Licensed under MIT"
            )
        )
    
    def _show_about(self, widget):
        """Show about dialog"""
        asyncio.ensure_future(self._show_about_dialog())


def main():
    """Main entry point for Agent-Toga"""
    return AgentTogaApp(
        formal_name="Agent-Toga",
        app_id="ai.agent.toga",
        app_name="agent_toga",
        author="Agent Zero Project",
        version="1.0.0",
        description="A native GUI for Agent Zero with Himiko Toga personality",
        home_page="https://github.com/o9nn/a9z"
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
