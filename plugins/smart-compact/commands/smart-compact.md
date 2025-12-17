---
description: Analyze conversation and auto-execute /compact with smart preservation instructions
---

# Smart Compact Analysis

You are about to help prepare for context compaction. Analyze the current conversation thoroughly and generate preservation instructions.

## Your Task

0. **FIRST - Capture tmux session** - Run this bash command IMMEDIATELY before doing anything else:
   ```bash
   tmux display-message -p '#S' > ~/.claude/smart-compact-session.txt 2>/dev/null || echo "" > ~/.claude/smart-compact-session.txt
   ```
   This saves the tmux session name for background command sending (no focus stealing).

1. **Analyze the conversation** - Review what we've been working on:
   - What files have been edited or created?
   - What key decisions were made?
   - What tasks are in progress or pending?
   - What important context would be lost if not preserved?

2. **Generate compact instructions** - Create a concise set of instructions for /compact that preserves:
   - Current task state and progress
   - Key file paths and their purposes
   - Important decisions and their rationale
   - Any TODO items or next steps
   - Technical context needed to continue work

3. **Save instructions to file** - Write the instructions to `~/.claude/smart-compact-instructions.txt` (cross-platform path)

4. **Auto-execute compact** - After saving, run this command to trigger the compact:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/auto-compact.py"
   ```

5. **Notify the user** - Output:
   ```
   Smart compact instructions saved and auto-compact triggered.
   The /compact command will execute automatically.
   ```

## Format for Instructions

Keep instructions concise but comprehensive. Example format:

```
Preserve: [Main task/goal being worked on]
Files: [Key files being modified with brief purpose]
Progress: [Current state - what's done, what's next]
Context: [Critical technical details needed to continue]
Decisions: [Key choices made and why]
Continue: [Explicit instruction for what to do after compact - e.g., "Continue implementing X" or "Resume fixing the bug in Y"]
```

## Important

- Be thorough but concise - compact instructions should be ~100-300 words
- Focus on what's needed to CONTINUE the work, not a full history
- Include specific file paths, function names, or technical details that would be hard to rediscover
- If there are pending TODOs, include them explicitly
- **ALWAYS include a "Continue:" instruction** - this ensures Claude continues working automatically after compact completes instead of waiting for user input
