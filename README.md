# KP's Claude Code Plugins

Community plugins for [Claude Code](https://claude.ai/code).

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add https://github.com/kp222x/claude-plugins
```

Then install any plugin:

```bash
/plugin install <plugin-name>
```

## Available Plugins

### smart-compact

Intelligent context compaction with auto-execution.

**Features:**
- Analyzes your conversation to identify what context to preserve
- Generates smart preservation instructions
- Automatically executes `/compact` with those instructions

**Install:**
```bash
/plugin install smart-compact
```

**Usage:**
```bash
/smart-compact
```

[Read more](./plugins/smart-compact/README.md)

---

## Contributing

Feel free to open issues or PRs for new plugins or improvements.

## License

MIT
