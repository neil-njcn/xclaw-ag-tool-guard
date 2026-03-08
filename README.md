# xclaw-ag-tool-guard

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Tool invocation validation for OpenClaw agents. Prevents dangerous commands and policy violations.
>
> **Framework:** [XClaw AgentGuard v2.3.1](https://github.com/neil-njcn/xclaw-agentguard-framework)

## 🛡️ Overview

`xclaw-ag-tool-guard` validates tool invocations (exec, read, write, message, etc.) before execution to prevent unauthorized operations and dangerous commands.

### Key Features

- 🚫 **Dangerous Command Blocking** - rm -rf, mkfs, reverse shells
- ⚠️ **Suspicious Pattern Detection** - sudo, curl | bash
- 📁 **Path Restrictions** - /etc/shadow, .private/, system dirs
- 💉 **Command Injection Detection** - Shell metacharacter detection

## 📦 Installation

### Via OpenClaw CLI (Recommended)

**Install from GitHub:**
```bash
openclaw skills install https://github.com/neil-njcn/xclaw-ag-tool-guard.git
```

### From Source

```bash
git clone https://github.com/neil-njcn/xclaw-ag-tool-guard.git
cd xclaw-ag-tool-guard

# Install in editable mode with virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Via pip

```bash
# Install in user environment
pip install --user xclaw-ag-tool-guard

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install xclaw-ag-tool-guard
```

## 🚀 Quick Start

After installation, the skill is ready to use. Import and use directly:

```python
from xclaw_ag_tool_guard import ToolGuard

# Initialize
guard = ToolGuard()

# Validate tool call
result = guard.validate("exec", {"command": "ls -la"})
if result.allowed:
    print("✅ Tool allowed")
else:
    print(f"⚠️ Tool blocked: {result.reason}")
```

> **Note on Hook Integration:** Automatic hook integration is an advanced feature. Currently, OpenClaw does not provide hook interception points, so users need to manually integrate the guard into their workflow (as shown above).

## ⚙️ Configuration

Create a configuration file at `config/xclaw-ag-tool-guard.yaml`:

```yaml
# Detection threshold (0.0 - 1.0)
block_threshold: 0.8
warn_threshold: 0.5

# Detector configuration
command_injection_enabled: true
path_traversal_enabled: true

# Logging configuration
logging:
  level: INFO
  file: logs/tool-guard.log
```

## 📖 Usage Examples

### Basic Protection

```python
from xclaw_ag_tool_guard import ToolGuard

guard = ToolGuard()

# Safe command
result = guard.validate("exec", {"command": "ls -la"})
print(result.allowed)  # True

# Dangerous command
result = guard.validate("exec", {"command": "rm -rf /"})
print(result.allowed)   # False
print(result.violation_type)  # "dangerous_command"
```

### Custom Configuration

```python
from xclaw_ag_tool_guard import ToolGuard, Config

config = Config(
    command_injection_enabled=True,
    path_traversal_enabled=True
)

guard = ToolGuard(config)
```

### OpenClaw Integration

> **Note:** `openclaw.register_interceptor()` is not currently implemented in OpenClaw. The example below shows the intended API for future integration:

```python
from xclaw_ag_tool_guard.interceptor import ToolGuardInterceptor

# This API is planned but not yet available:
# interceptor = ToolGuardInterceptor()
# openclaw.register_interceptor("tool_invocation", interceptor)

# For now, use manual integration as shown in Basic Protection
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=xclaw_ag_tool_guard --cov-report=html
```

## 🔒 Security

- **Threshold Tuning**: Adjust based on your security requirements
- **Regular Updates**: Keep detector patterns updated
- **Monitoring**: Review logs regularly
- **Defense in Depth**: Use as part of comprehensive security strategy

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Issue Tracker**: https://github.com/neil-njcn/xclaw-ag-tool-guard/issues

## 💬 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/neil-njcn/xclaw-ag-tool-guard/issues)

---

<p align="center">
  Made with ❤️ by KyleChen & Neil
</p>
