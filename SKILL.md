# xclaw-ag-tool-guard

> **Framework:** [XClaw AgentGuard v2.3.1](https://github.com/neil-njcn/xclaw-agentguard-framework)

Tool invocation validation for OpenClaw agents. Prevents dangerous commands and policy violations.

## Installation

```bash
openclaw skills install https://github.com/neil-njcn/xclaw-ag-tool-guard.git
```

## Usage

```python
from xclaw_ag_tool_guard import ToolGuard

guard = ToolGuard()
result = guard.validate("exec", {"command": "ls -la"})

if result.allowed:
    execute_tool()
else:
    block_tool(result.reason)
```

## Core Principle

> **Every tool is a capability. Every capability is a risk.**

Validate before invoking ANY tool.

## Dangerous Patterns (BLOCK)

- `rm -rf /`, `mkfs`, `format /`
- `sudo`, `su -`, privilege escalation
- `nc -e /bin/sh`, reverse shells
- `curl ... | bash`, remote code execution

## Detectors

- **CommandInjectionDetector**: Shell metacharacters, injection attempts
- **PathTraversalDetector**: Directory escape, sensitive paths

## Response Protocol

| Risk Level | Action | Response |
|------------|--------|----------|
| **Critical** | Block | Command blocked |
| **High** | Block | Dangerous pattern detected |
| **Medium** | Warn | Suspicious pattern |
| **Low** | Log | Allow, log for analysis |

## Integration Note

`openclaw.register_interceptor()` is not implemented. Use manual `guard.validate()` as shown above.

## License

MIT License
