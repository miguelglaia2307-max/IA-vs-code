"""
Error Recovery Agent - Uses AI to diagnose and fix errors automatically
"""
import os
from typing import Optional, Dict, Any
from app.services.logger import logger
from datetime import datetime

# Optional OpenAI import - gracefully handle missing API key
try:
    from openai import OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except Exception as e:
    logger.log_warning("OpenAI client initialization failed", {"error": str(e)})
    client = None

class ErrorRecoveryAgent:
    """AI-powered agent that diagnoses and suggests fixes for errors"""
    
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.3
    
    def analyze_error(self, error_type: str, message: str, context: Optional[Dict[str, Any]] = None, traceback_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze an error using AI and provide diagnosis and recommendations
        """
        # Check if OpenAI client is available
        if not client:
            return {
                "status": "degraded",
                "analysis": "AI error analysis unavailable (OpenAI API key not configured)",
                "error_type": error_type,
                "timestamp": datetime.utcnow().isoformat(),
                "note": "Configure OPENAI_API_KEY environment variable to enable AI analysis"
            }
        
        try:
            # Build context string
            context_str = ""
            if context:
                context_str = f"\n\nContext: {context}"
            
            traceback_section = ""
            if traceback_str:
                traceback_section = f"\n\nTraceback:\n{traceback_str}"
            
            prompt = f"""You are a skilled Python and FastAPI developer debugging an application error.

Error Type: {error_type}
Error Message: {message}{context_str}{traceback_section}

Provide a detailed analysis with:
1. Root cause analysis (2-3 sentences)
2. Severity level (low/medium/high/critical)
3. Immediate fix (if applicable)
4. Prevention strategy
5. Code snippet (if applicable)

Format your response as JSON with keys: root_cause, severity, immediate_fix, prevention, code_snippet"""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Python debugger and code reviewer. Provide practical, actionable solutions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Log the analysis
            logger.log_info("AI Analysis completed for error", {
                "error_type": error_type,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return {
                "status": "success",
                "analysis": analysis_text,
                "error_type": error_type,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.log_error("AI_ANALYSIS_FAILED", str(e), {"error_type": error_type})
            return {
                "status": "error",
                "message": f"Failed to analyze error: {str(e)}",
                "error_type": error_type
            }
    
    def suggest_fix(self, error_type: str, message: str, previous_attempts: Optional[list] = None) -> Dict[str, Any]:
        """
        Suggest a specific fix for an error based on previous attempts
        """
        # Check if OpenAI client is available
        if not client:
            return {
                "status": "degraded",
                "fix": "AI fix suggestion unavailable (OpenAI API key not configured)",
                "error_type": error_type,
                "timestamp": datetime.utcnow().isoformat(),
                "note": "Configure OPENAI_API_KEY environment variable to enable AI analysis"
            }
        
        try:
            attempts_str = ""
            if previous_attempts:
                attempts_str = "\n\nPrevious failed attempts:\n" + "\n".join(previous_attempts)
            
            prompt = f"""Given this error in a FastAPI Python application:

Error Type: {error_type}
Error Message: {message}{attempts_str}

Suggest a specific, implementable fix. Be concise and practical.
Provide ONLY the solution code or steps, no explanation."""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Python expert. Provide only actionable code fixes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            fix_text = response.choices[0].message.content
            
            logger.log_info("AI Fix suggestion generated", {"error_type": error_type})
            
            return {
                "status": "success",
                "fix": fix_text,
                "error_type": error_type,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.log_error("AI_FIX_SUGGESTION_FAILED", str(e), {"error_type": error_type})
            return {
                "status": "error",
                "message": f"Failed to generate fix: {str(e)}"
            }
    
    def health_check(self) -> bool:
        """Check if AI service is available"""
        if not client:
            return False
        try:
            response = client.models.list()
            return True
        except Exception as e:
            logger.log_warning("AI Service health check failed", {"error": str(e)})
            return False

# Global agent instance
error_agent = ErrorRecoveryAgent()
