#!/usr/bin/env python3
"""
Auto-Compact Script for Smart Compact Plugin
Cross-platform script to automatically execute /compact with generated instructions.

Primary method: tmux send-keys (background, no focus stealing)
Fallback: pyautogui keyboard simulation (requires focus)
"""

import os
import sys
import time
import platform
import subprocess
import shutil
from pathlib import Path

# Configuration
CLAUDE_DIR = Path.home() / ".claude"
INSTRUCTIONS_FILE = str(CLAUDE_DIR / "smart-compact-instructions.txt")
SESSION_FILE = str(CLAUDE_DIR / "smart-compact-session.txt")
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


def read_tmux_session():
    """Read the tmux session name if available."""
    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, 'r') as f:
        session = f.read().strip()

    return session if session else None


def escape_instructions(instructions: str) -> str:
    """Escape instructions for safe input."""
    # Replace newlines with spaces
    escaped = instructions.replace('\n', ' ')
    # Collapse multiple spaces
    escaped = ' '.join(escaped.split())
    return escaped


def tmux_available():
    """Check if tmux is available."""
    return shutil.which('tmux') is not None


def tmux_session_exists(session: str) -> bool:
    """Check if a tmux session exists."""
    try:
        result = subprocess.run(
            ['tmux', 'has-session', '-t', session],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def send_via_tmux(session: str, command: str) -> bool:
    """Send command to tmux session. Returns True on success."""
    try:
        # Send the command
        subprocess.run(
            ['tmux', 'send-keys', '-t', session, command, 'Enter'],
            check=True,
            capture_output=True,
            timeout=10
        )
        return True
    except Exception as e:
        print(f"tmux send-keys failed: {e}")
        return False


def send_via_pyautogui(command: str):
    """Send command via keyboard simulation (fallback)."""
    try:
        import pyautogui
    except ImportError:
        print("ERROR: pyautogui not installed. Run: pip install pyautogui")
        show_notification("Smart Compact", "pyautogui not installed. Run: pip install pyautogui")
        sys.exit(1)

    # Small delay to ensure terminal is focused
    time.sleep(0.3)

    # Type the command
    pyautogui.write(command, interval=0.01)

    # Press Enter to execute
    time.sleep(0.1)
    pyautogui.press('enter')


def cleanup():
    """Remove temp files after use."""
    for f in [INSTRUCTIONS_FILE, SESSION_FILE]:
        try:
            os.remove(f)
        except OSError:
            pass


def main():
    """Main execution flow."""
    print("Smart Compact: Starting auto-execution...")

    # Validate instructions file
    check_instructions_file()

    # Read instructions
    instructions = read_instructions()
    escaped = escape_instructions(instructions)
    compact_cmd = f"/compact {escaped}"

    # Try tmux first (preferred - background, no focus stealing)
    tmux_session = read_tmux_session()

    if tmux_session and tmux_available() and tmux_session_exists(tmux_session):
        print(f"Smart Compact: Using tmux session '{tmux_session}'")

        # Send compact command
        if send_via_tmux(tmux_session, compact_cmd):
            print("Smart Compact: Sent /compact command")

            # Wait for compact to process
            time.sleep(6)

            # Send continue command
            if send_via_tmux(tmux_session, "continue"):
                print("Smart Compact: Sent 'continue' command")

            cleanup()
            show_notification("Smart Compact", "Compact executed via tmux (background)")
            print("Smart Compact: Complete!")
            return
        else:
            print("Smart Compact: tmux failed, falling back to pyautogui")

    # Fallback to pyautogui (requires focus)
    print("Smart Compact: Using pyautogui (focus required)")
    show_notification("Smart Compact", "Using keyboard simulation - keep terminal focused")

    send_via_pyautogui(compact_cmd)

    # Wait for compact to process
    time.sleep(6)

    # Send continue
    send_via_pyautogui("continue")

    cleanup()
    show_notification("Smart Compact", "Compact command executed")
    print("Smart Compact: Complete!")


if __name__ == "__main__":
    main()
