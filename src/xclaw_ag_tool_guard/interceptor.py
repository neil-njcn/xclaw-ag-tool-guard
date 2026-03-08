"""
Tool guard interceptor for OpenClaw integration.
"""

import logging
from typing import Any, Dict, Optional

from .config import Config
from .detector import ToolGuard, ValidationResult


class ToolGuardInterceptor:
    """Interceptor for OpenClaw tool invocations."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.guard = ToolGuard(self.config)
        self.logger = logging.getLogger(__name__)
    
    def intercept(self, tool_name: str, arguments: Dict[str, Any],
                  context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Intercept and validate tool invocation."""
        result = self.guard.validate(tool_name, arguments, context)
        
        if not result.allowed:
            self.logger.warning(f"Tool blocked: {result.reason}")
        
        return {
            'allowed': result.allowed,
            'result': result.to_dict(),
        }
