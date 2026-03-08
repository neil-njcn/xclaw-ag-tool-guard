"""
Tests for xclaw-ag-tool-guard
"""

import pytest
from xclaw_ag_tool_guard import ToolGuard, ValidationResult, Config


def test_config_defaults():
    """Test default configuration"""
    config = Config()
    assert config.block_threshold == 0.8
    assert config.command_injection_enabled is True


def test_guard_initialization():
    """Test guard initialization"""
    guard = ToolGuard()
    assert guard is not None


def test_safe_command_allowed():
    """Test safe command allowed"""
    guard = ToolGuard()
    result = guard.validate("exec", {"command": "ls -la"})
    assert result.allowed


def test_config_validation():
    """Test configuration validation"""
    with pytest.raises(ValueError):
        Config(block_threshold=1.5)
