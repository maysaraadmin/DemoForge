#!/usr/bin/env python3
"""
DemoForge GUI Manager Launcher
"""
import sys
import os

def main():
    """Launch the DemoForge GUI Manager"""
    # Add current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

    try:
        from gui_manager import main
        main()
    except ImportError as e:
        print(f"Error: Missing required modules. Please install dependencies:")
        print("pip install -r requirements.txt")
        print(f"Error details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
