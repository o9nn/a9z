#!/usr/bin/env python3
"""
Agent-Toga Launcher

Launch the Agent-Toga native GUI application.

Usage:
    python run_toga.py
    
Requirements:
    pip install toga
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import toga
        return True
    except ImportError:
        print("Error: Toga is not installed.")
        print("Please install it with: pip install toga")
        print("\nFor specific platforms:")
        print("  macOS:   pip install toga-cocoa")
        print("  Linux:   pip install toga-gtk")
        print("  Windows: pip install toga-winforms")
        return False

def main():
    """Main entry point"""
    if not check_dependencies():
        sys.exit(1)
    
    from python.gui.agent_toga import main as toga_main
    app = toga_main()
    app.main_loop()

if __name__ == "__main__":
    main()
