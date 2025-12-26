"""
Tests for Agent-Toga GUI

Tests the Toga GUI components and personality module.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestTogaPersonality:
    """Tests for the Toga personality module"""
    
    def test_personality_import(self):
        """Test that personality module can be imported"""
        from python.gui.toga_personality import TogaPersonality, Mood
        assert TogaPersonality is not None
        assert Mood is not None
    
    def test_personality_greetings(self):
        """Test greeting generation"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        greeting = personality.get_greeting()
        
        assert isinstance(greeting, str)
        assert len(greeting) > 0
    
    def test_personality_task_complete(self):
        """Test task completion responses"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        response = personality.get_task_complete_response()
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_personality_error_response(self):
        """Test error responses"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        response = personality.get_error_response()
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_topic_detection_code(self):
        """Test code topic detection"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        
        assert personality.detect_topic("Write a Python function") == "code"
        assert personality.detect_topic("Create a class for me") == "code"
        assert personality.detect_topic("Help me with this script") == "code"
    
    def test_topic_detection_security(self):
        """Test security topic detection"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        
        assert personality.detect_topic("Run a security scan") == "security"
        assert personality.detect_topic("Find vulnerabilities") == "security"
        assert personality.detect_topic("Pentest this system") == "security"
    
    def test_topic_detection_greeting(self):
        """Test greeting topic detection"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        
        assert personality.detect_topic("Hello there") == "greeting"
        assert personality.detect_topic("Hi, how are you?") == "greeting"
        assert personality.detect_topic("Hey!") == "greeting"
    
    def test_topic_detection_goodbye(self):
        """Test goodbye topic detection"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        
        assert personality.detect_topic("Goodbye") == "goodbye"
        assert personality.detect_topic("I need to quit") == "goodbye"
        assert personality.detect_topic("Exit the program") == "goodbye"
    
    def test_contextual_response(self):
        """Test contextual response generation"""
        from python.gui.toga_personality import TogaPersonality
        
        personality = TogaPersonality()
        
        # Should return a string response
        response = personality.get_contextual_response("Hello!")
        assert isinstance(response, str)
        
        response = personality.get_contextual_response("Write some code")
        assert isinstance(response, str)
    
    def test_mood_enum(self):
        """Test Mood enum values"""
        from python.gui.toga_personality import Mood
        
        assert Mood.EXCITED.value == "excited"
        assert Mood.CURIOUS.value == "curious"
        assert Mood.PLAYFUL.value == "playful"
        assert Mood.FOCUSED.value == "focused"
        assert Mood.MISCHIEVOUS.value == "mischievous"
        assert Mood.HELPFUL.value == "helpful"
    
    def test_format_response(self):
        """Test response formatting"""
        from python.gui.toga_personality import TogaPersonality, Mood
        
        personality = TogaPersonality()
        
        # Test with different moods
        response = personality.format_response("Test message", Mood.EXCITED)
        assert "Ehehe~" in response or "Test message" in response
        
        response = personality.format_response("Test message", Mood.FOCUSED)
        assert "Test message" in response


class TestTogaQuotes:
    """Tests for the Toga quotes collection"""
    
    def test_quotes_import(self):
        """Test that quotes can be imported"""
        from python.gui.toga_personality import TogaQuotes
        assert TogaQuotes is not None
    
    def test_random_quote(self):
        """Test random quote generation"""
        from python.gui.toga_personality import TogaQuotes
        
        quote = TogaQuotes.get_random_quote()
        assert isinstance(quote, str)
        assert len(quote) > 0
    
    def test_tech_quote(self):
        """Test tech quote generation"""
        from python.gui.toga_personality import TogaQuotes
        
        quote = TogaQuotes.get_tech_quote()
        assert isinstance(quote, str)
        assert len(quote) > 0


class TestAgentTogaApp:
    """Tests for the main Agent-Toga application"""
    
    def test_app_import(self):
        """Test that app module can be imported"""
        try:
            from python.gui.agent_toga import AgentTogaApp
            assert AgentTogaApp is not None
        except ImportError as e:
            # Toga may not be installed in test environment
            if "toga" in str(e).lower():
                pytest.skip("Toga not installed")
            raise
    
    def test_main_function(self):
        """Test that main function exists"""
        try:
            from python.gui.agent_toga import main
            assert callable(main)
        except ImportError as e:
            if "toga" in str(e).lower():
                pytest.skip("Toga not installed")
            raise


class TestModuleExports:
    """Tests for module exports"""
    
    def test_gui_module_exports(self):
        """Test that gui module exports correctly"""
        try:
            from python.gui import AgentTogaApp, main, __version__
            assert AgentTogaApp is not None
            assert main is not None
            assert __version__ == "1.0.0"
        except ImportError as e:
            if "toga" in str(e).lower():
                pytest.skip("Toga not installed")
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
