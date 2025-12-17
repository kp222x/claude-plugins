# Smart Compact Plugin

Intelligent context compaction for Claude Code with auto-execution.

## What it does

When your conversation context is getting full, this plugin:
1. Analyzes your current conversation
2. Generates smart preservation instructions (what to keep)
3. Automatically executes `/compact` with those instructions

## Installation

```bash
# Add the marketplace
/plugin marketplace add https://github.com/kp222x/claude-plugins

# Install the plugin
/plugin install smart-compact
```

## Requirements

The auto-execution feature requires `pyautogui`:

```bash
pip install pyautogui
```

**Platform-specific notes:**
- **macOS**: Works out of the box (may need accessibility permissions)
- **Windows**: Works with pyautogui
- **Linux**: May need `python3-tk` and `python3-dev` packages

## Usage

When you want to compact with smart context preservation:

```
/smart-compact
```

The plugin will:
1. Analyze what you've been working on
2. Identify key files, decisions, and context to preserve
3. Generate compact instructions
4. Automatically execute `/compact` with those instructions

## How it works

1. **Analysis Phase**: Claude reviews the conversation to identify:
   - Files edited or created
   - Key decisions made
   - Tasks in progress
   - Important technical context

2. **Instruction Generation**: Creates a concise summary (~100-300 words) focusing on what's needed to continue the work

3. **Auto-Execution**: Uses `pyautogui` to type and execute the `/compact` command with the generated instructions

## Manual Alternative

If auto-execution doesn't work on your system, you can:
1. Run `/smart-compact`
2. Copy the instructions from `~/.claude/smart-compact-instructions.txt`
3. Manually run `/compact [paste instructions]`

## Cross-Platform Support

| Platform | Keyboard Simulation | Notifications |
|----------|---------------------|---------------|
| macOS | pyautogui | osascript |
| Windows | pyautogui | win10toast |
| Linux | pyautogui | notify-send |

## License

MIT
