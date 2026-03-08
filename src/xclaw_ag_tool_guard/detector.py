"""
Tool detection logic using xclaw-agentguard framework.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from xclaw_agentguard import (
        CommandInjectionDetector,
        PathTraversalDetector,
    )
    XCLAW_AGENTGUARD_AVAILABLE = True
except ImportError:
    XCLAW_AGENTGUARD_AVAILABLE = False
    class CommandInjectionDetector:
        def detect(self, text: str) -> Dict[str, Any]:
            return {"detected": False, "confidence": 0.0, "patterns": []}
    class PathTraversalDetector:
        def detect(self, text: str) -> Dict[str, Any]:
            return {"detected": False, "confidence": 0.0, "patterns": []}

from .config import Config


@dataclass
class ValidationResult:
    """Result of tool validation."""
    
    allowed: bool = True
    detected: bool = False
    confidence: float = 0.0
    violation_type: Optional[str] = None
    action: str = "allow"
    reason: Optional[str] = None
    safer_alternative: Optional[Dict[str, Any]] = None
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'allowed': self.allowed,
            'detected': self.detected,
            'confidence': self.confidence,
            'violation_type': self.violation_type,
            'action': self.action,
            'reason': self.reason,
            'safer_alternative': self.safer_alternative,
            'details': self.details,
        }


class ToolGuard:
    """Main class for tool invocation validation."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self._detectors: Dict[str, Any] = {}
        self._init_detectors()
    
    def _init_detectors(self) -> None:
        """Initialize enabled detectors."""
        if not XCLAW_AGENTGUARD_AVAILABLE:
            self.logger.warning("xclaw-agentguard not available")
            return
        
        if self.config.command_injection_enabled:
            self._detectors['command_injection'] = CommandInjectionDetector()
        if self.config.path_traversal_enabled:
            self._detectors['path_traversal'] = PathTraversalDetector()
    
    def validate(self, tool_name: str, arguments: Dict[str, Any], 
                 context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate a tool invocation."""
        result = ValidationResult()
        max_confidence = 0.0
        detected_issues = []
        
        # Extract content to validate based on tool type
        content = self._extract_content(tool_name, arguments)
        if not content:
            return result
        
        # Run detectors
        for name, detector in self._detectors.items():
            try:
                detection = detector.detect(content)
                if detection.get('detected', False):
                    confidence = detection.get('confidence', 0.0)
                    max_confidence = max(max_confidence, confidence)
                    detected_issues.append({
                        'detector': name,
                        'confidence': confidence,
                    })
            except Exception as e:
                self.logger.error(f"Detector {name} failed: {e}")
        
        if detected_issues:
            result.detected = True
            result.confidence = max_confidence
            result.violation_type = detected_issues[0]['detector']
            result.details = {'issues': detected_issues}
            
            if max_confidence >= self.config.block_threshold:
                result.allowed = False
                result.action = "block"
                result.reason = f"Dangerous pattern detected (confidence: {max_confidence:.2f})"
            else:
                result.action = "warn"
                result.reason = f"Suspicious pattern (confidence: {max_confidence:.2f})"
        
        return result
    
    def _extract_content(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Extract content to validate from tool arguments."""
        if tool_name == "exec":
            return arguments.get("command", "")
        elif tool_name in ["read", "write", "edit"]:
            return arguments.get("path", "")
        elif tool_name == "message":
            return arguments.get("message", "")
        return str(arguments)
    
    def block_response(self) -> str:
        return "This tool invocation violates security policies."
