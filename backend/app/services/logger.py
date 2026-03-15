import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

class CentralLogger:
    """Centralized logging system for the application"""
    
    def __init__(self):
        self.logger = logging.getLogger("prompt_optimizer")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / "app.log")
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Error log file
        self.error_file = log_dir / "errors.jsonl"
    
    def log_error(self, error_type: str, message: str, context: Optional[Dict[str, Any]] = None, traceback_str: Optional[str] = None):
        """Log an error in both text and JSON format"""
        self.logger.error(f"{error_type}: {message}")
        
        error_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": error_type,
            "message": message,
            "context": context or {},
            "traceback": traceback_str
        }
        
        with open(self.error_file, "a") as f:
            f.write(json.dumps(error_record) + "\n")
    
    def log_info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log info message"""
        self.logger.info(message)
        if context:
            self.logger.debug(f"Context: {context}")
    
    def log_warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log warning message"""
        self.logger.warning(message)
        if context:
            self.logger.debug(f"Context: {context}")
    
    def get_recent_errors(self, limit: int = 50) -> list:
        """Get recent errors from log file"""
        errors = []
        try:
            with open(self.error_file, "r") as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    errors.append(json.loads(line))
        except FileNotFoundError:
            pass
        return errors

# Global logger instance
logger = CentralLogger()
