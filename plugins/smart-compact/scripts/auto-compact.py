#!/usr/bin/env python3
"""
Auto-Compact Script for Smart Compact Plugin
Cross-platform script to automatically execute /compact with generated instructions.

Requires: pip install pyautogui
"""

import os
import sys
import time
import platform

# Configuration
INSTRUCTIONS_FILE = "/tmp/smart-compact-instructions.txt"
MAX_AGE_SECONDS = 600  # 10 minutes


def get_platform():
    """Detect the current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"


def show_notification(title: str, message: str):
    """Show a platform-appropriate notification."""
    plat = get_platform()

    if plat == "macos":
        os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
    elif plat == "windows":
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=3)
        except ImportError:
            print(f"[{title}] {message}")
    else:  # Linux
        try:
            os.system(f'notify-send "{title}" "{message}"')
        except Exception:
            print(f"[{title}] {message}")


def check_instructions_file():
    """Validate the instructions file exists and is recent."""
    if not os.path.exists(INSTRUCTIONS_FILE):
        show_notification("Smart Compact", "No instructions file found. Run /smart-compact first.")
        sys.exit(1)

    # Check file age
    file_age = time.time() - os.path.getmtime(INSTRUCTIONS_FILE)
    if file_age > MAX_AGE_SECONDS:
        show_notification("Smart Compact", f"Instructions are stale (>{MAX_AGE_SECONDS//60} min old). Run /smart-compact again.")
        sys.exit(1)

    return True


def read_instructions():
    """Read and validate instructions from file."""
    with open(INSTRUCTIONS_FILE, 'r') as f:
        instructions = f.read().strip()

    if not instructions:
        show_notification("Smart Compact", "Instructions file is empty.")
        sys.exit(1)

    return instructions


def escape_instructions(instructions: str) -> str:
    """Escape instructions for safe keyboard input."""
    # Replace newlines with spaces
    escaped = instructions.replace('\n', ' ')
    # Collapse multiple spaces
    escaped = ' '.join(escaped.split())
    return escaped


def type_compact_command(instructions: str):
    """Type the /compact command using pyautogui."""
    try:
        import pyautogui
    except ImportError:
        print("ERROR: pyautogui not installed. Run: pip install pyautogui")
        show_notification("Smart Compact", "pyautogui not installed. Run: pip install pyautogui")
        sys.exit(1)

    # Small delay to ensure terminal is focused
    time.sleep(0.3)

    # Type the compact command
    compact_cmd = f"/compact {instructions}"

    # Use typewrite for cross-platform compatibility
    # Note: pyautogui.write() is an alias for typewrite()
    pyautogui.write(compact_cmd, interval=0.01)

    # Press Enter to execute
    time.sleep(0.1)
    pyautogui.press('enter')


def cleanup():
    """Remove the instructions file after use."""
    try:
        os.remove(INSTRUCTIONS_FILE)
    except OSError:
        pass


def main():
    """Main execution flow."""
    print("Smart Compact: Starting auto-execution...")

    # Validate file
    check_instructions_file()

    # Read instructions
    instructions = read_instructions()

    # Escape for keyboard input
    escaped = escape_instructions(instructions)

    # Type the command
    type_compact_command(escaped)

    # Cleanup
    cleanup()

    # Notify success
    show_notification("Smart Compact", "Compact command executed")
    print("Smart Compact: Complete!")


if __name__ == "__main__":
    main()
