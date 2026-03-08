"""
xclaw-ag-tool-guard: Tool invocation validation for OpenClaw agents.

This package provides tool operation validation to prevent dangerous commands
and policy violations.
"""

from .config import Config
from .detector import ToolGuard, ValidationResult
from .interceptor import ToolGuardInterceptor

__version__ = "1.0.0"
__author__ = "xclaw"
__email__ = "dev@xclaw.dev"

__all__ = [
    "Config",
    "ToolGuard",
    "ValidationResult",
    "ToolGuardInterceptor",
]


class ToolGuardSkill:
    """
    OpenClaw skill entry point for xclaw-ag-tool-guard.
    """
    
    name = "xclaw-ag-tool-guard"
    version = __version__
    description = "Tool invocation validation for OpenClaw agents"
    
    def __init__(self, config: dict = None):
        from .config import Config
        from .interceptor import ToolGuardInterceptor
        
        if config:
            self.config = Config.from_dict(config)
        else:
            self.config = Config()
        
        self.interceptor = ToolGuardInterceptor(self.config)
    
    def register(self, openclaw_app):
        openclaw_app.register_interceptor("tool_invocation", self.interceptor)
    
    def get_interceptor(self):
        return self.interceptor
