"""
Advanced AI Agents for Prompt Optimization Platform

This module implements multiple specialized AI agents:
1. PromptGenerationAgent - Generates intelligent prompt variations
2. ResultAnalysisAgent - Analyzes optimization results
3. AdaptiveOptimizationAgent - Adapts optimization strategy
4. QualityValidationAgent - Validates prompt quality
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import logging

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

class AIAgentType(Enum):
    PROMPT_GENERATION = "prompt_generation"
    RESULT_ANALYSIS = "result_analysis"
    ADAPTIVE_OPTIMIZATION = "adaptive_optimization"
    QUALITY_VALIDATION = "quality_validation"

class BaseAIAgent(ABC):
    """Abstract base class for AI agents"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        self.agent_type = None
        self.execution_history = []
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the agent's primary task"""
        pass
    
    def log_execution(self, input_data: Any, output_data: Any, status: str = "success"):
        """Log agent execution for debugging and analysis"""
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent_type": self.agent_type,
            "input": input_data,
            "output": output_data,
            "status": status
        })
    
    def call_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call OpenAI LLM with error handling"""
        if not self.client:
            logger.warning(f"OpenAI client not available for {self.agent_type}")
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return None

class PromptGenerationAgent(BaseAIAgent):
    """Agent specialized in generating optimized prompt variations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = AIAgentType.PROMPT_GENERATION
    
    def execute(
        self,
        initial_prompt: str,
        num_variations: int = 5,
        optimization_focus: List[str] = None,
        previous_results: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate intelligent prompt variations based on optimization history
        
        Args:
            initial_prompt: Base prompt to optimize
            num_variations: Number of variations to generate
            optimization_focus: Areas to focus on (clarity, specificity, etc)
            previous_results: Previous optimization results for context
            
        Returns:
            Dict containing generated variations and metadata
        """
        
        focus_text = ""
        if optimization_focus:
            focus_text = f"\nOptimization Focus Areas: {', '.join(optimization_focus)}"
        
        context_text = ""
        if previous_results:
            best_score = max([r.get("score", 0) for r in previous_results], default=0)
            best_prompt = next((r.get("prompt", "") for r in previous_results if r.get("score") == best_score), "")
            context_text = f"\nPrevious Best Result (Score: {best_score}):\n{best_prompt}\n"
        
        system_prompt = """You are an expert prompt engineer specializing in optimization. 
Your task is to generate diverse, high-quality prompt variations that improve upon the original 
while maintaining semantic meaning. Focus on clarity, specificity, and effectiveness.

Generate variations that:
1. Improve instruction clarity
2. Add specific constraints or requirements
3. Enhance context and examples
4. Optimize for different LLM behaviors
5. Are measurably better based on the optimization focus areas

Return ONLY a valid JSON array of strings, with no additional text."""
        
        user_prompt = f"""Generate exactly {num_variations} variations of this prompt:

ORIGINAL PROMPT:
{initial_prompt}
{context_text}{focus_text}

Return response as JSON array: ["variation1", "variation2", ...]"""
        
        response = self.call_llm(system_prompt, user_prompt, temperature=0.85, max_tokens=2500)
        
        variations = []
        if response:
            try:
                variations = json.loads(response)
                if not isinstance(variations, list):
                    variations = [variations]
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from response
                import re
                match = re.search(r'\[.*\]', response, re.DOTALL)
                if match:
                    try:
                        variations = json.loads(match.group())
                    except:
                        variations = [initial_prompt] * num_variations
        
        result = {
            "agent": "PromptGenerationAgent",
            "variations": variations[:num_variations],
            "num_variations_generated": len(variations),
            "timestamp": datetime.now().isoformat()
        }
        
        self.log_execution({
            "initial_prompt": initial_prompt[:100],
            "focus": optimization_focus
        }, result)
        
        return result

class ResultAnalysisAgent(BaseAIAgent):
    """Agent specialized in analyzing optimization results"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = AIAgentType.RESULT_ANALYSIS
    
    def execute(
        self,
        optimization_results: List[Dict],
        dataset_size: int,
        evaluation_metric: str
    ) -> Dict[str, Any]:
        """
        Analyze optimization results and provide insights
        
        Args:
            optimization_results: List of variations with scores
            dataset_size: Size of the dataset used
            evaluation_metric: Type of metric used
            
        Returns:
            Dict containing analysis and recommendations
        """
        
        if not optimization_results:
            return {"analysis": "No results to analyze", "recommendations": []}
        
        # Calculate statistics
        scores = [r.get("score", 0) for r in optimization_results]
        best_score = max(scores)
        worst_score = min(scores)
        avg_score = sum(scores) / len(scores)
        improvement = ((best_score - worst_score) / worst_score * 100) if worst_score > 0 else 0
        
        top_variations = sorted(optimization_results, key=lambda x: x.get("score", 0), reverse=True)[:3]
        
        system_prompt = """You are an expert data analyst specializing in AI prompt optimization. 
Analyze the optimization results and provide:
1. Key insights about the optimization process
2. Patterns in what improved performance
3. Specific, actionable recommendations for further optimization
4. Potential areas where the prompt could be overfit to the dataset

Be concise but insightful. Return as structured JSON."""
        
        user_prompt = f"""Analyze these prompt optimization results:

Dataset Size: {dataset_size}
Evaluation Metric: {evaluation_metric}
Number of Variations Tested: {len(optimization_results)}

Score Statistics:
- Best Score: {best_score:.2%}
- Worst Score: {worst_score:.2%}
- Average Score: {avg_score:.2%}
- Improvement Range: {improvement:.1f}%

Top 3 Variations:
{chr(10).join([f"- Score: {v.get('score'):.2%}, Prompt: {v.get('prompt', '')[:80]}..." for v in top_variations])}

Provide analysis as JSON with keys: insights, recommendations, convergence_assessment"""
        
        response = self.call_llm(system_prompt, user_prompt, temperature=0.6, max_tokens=1500)
        
        analysis = {"response": response}
        if response:
            try:
                analysis = json.loads(response)
            except:
                analysis = {"insights": response}
        
        result = {
            "agent": "ResultAnalysisAgent",
            "analysis": analysis,
            "statistics": {
                "best_score": best_score,
                "worst_score": worst_score,
                "average_score": avg_score,
                "improvement_range": improvement
            },
            "timestamp": datetime.now().isoformat()
        }
        
        self.log_execution({
            "num_results": len(optimization_results),
            "metric": evaluation_metric
        }, result)
        
        return result

class AdaptiveOptimizationAgent(BaseAIAgent):
    """Agent that adapts optimization strategy based on progress"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = AIAgentType.ADAPTIVE_OPTIMIZATION
    
    def execute(
        self,
        initial_score: float,
        current_best_score: float,
        iteration_count: int,
        convergence_plateau_iterations: int = 0,
        previous_focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        Determine adaptive optimization strategy
        
        Args:
            initial_score: Score of the initial prompt
            current_best_score: Best score achieved so far
            iteration_count: Current iteration number
            convergence_plateau_iterations: How many iterations without improvement
            previous_focus_areas: Previously explored focus areas
            
        Returns:
            Dict with recommended next steps and focus areas
        """
        
        improvement = (current_best_score - initial_score) / initial_score if initial_score > 0 else 0
        
        system_prompt = """You are an expert in adaptive optimization strategies. 
Based on the optimization progress, recommend the best strategy for the next iteration.

Consider:
1. Whether convergence is happening
2. Token efficiency
3. Whether to explore new areas or refine existing ones
4. When to stop (diminishing returns)

Return JSON with: strategy, focus_areas, continue_optimization, confidence"""
        
        user_prompt = f"""Current Optimization Progress:

Iteration: {iteration_count}
Initial Score: {initial_score:.2%}
Current Best Score: {current_best_score:.2%}
Improvement: {improvement:.2%}
Iterations Without Improvement: {convergence_plateau_iterations}
Previously Explored: {', '.join(previous_focus_areas) if previous_focus_areas else 'None'}

Recommend the next optimization strategy."""
        
        response = self.call_llm(system_prompt, user_prompt, temperature=0.5, max_tokens=1200)
        
        strategy = {"response": response}
        if response:
            try:
                strategy = json.loads(response)
            except:
                strategy = {"strategy": response}
        
        result = {
            "agent": "AdaptiveOptimizationAgent",
            "strategy": strategy,
            "current_state": {
                "iteration": iteration_count,
                "improvement": improvement,
                "convergence_plateau": convergence_plateau_iterations
            },
            "timestamp": datetime.now().isoformat()
        }
        
        self.log_execution({
            "iteration": iteration_count,
            "improvement": improvement
        }, result)
        
        return result

class QualityValidationAgent(BaseAIAgent):
    """Agent specialized in validating prompt quality"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_type = AIAgentType.QUALITY_VALIDATION
    
    def execute(
        self,
        prompt: str,
        target_task: str,
        evaluation_results: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Validate prompt quality and identify potential issues
        
        Args:
            prompt: Prompt to validate
            target_task: What the prompt is designed to do
            evaluation_results: Results from evaluation dataset
            
        Returns:
            Dict with validation assessment
        """
        
        system_prompt = """You are a critical quality assurance expert for AI prompts.
Evaluate the prompt for:
1. Clarity and unambiguity
2. Completeness of instructions
3. Potential for misinterpretation
4. Overfitting to specific examples
5. Generalization capability
6. Potential biases

Return as JSON with: quality_score (0-1), issues, strengths, recommendations"""
        
        eval_context = ""
        if evaluation_results:
            success_rate = sum(1 for r in evaluation_results if r.get("passed")) / len(evaluation_results) if evaluation_results else 0
            eval_context = f"\nEvaluation Success Rate: {success_rate:.2%}"
        
        user_prompt = f"""Validate this prompt for the task: {target_task}

PROMPT:
{prompt}{eval_context}

Provide detailed quality assessment."""
        
        response = self.call_llm(system_prompt, user_prompt, temperature=0.4, max_tokens=1500)
        
        validation = {"response": response}
        if response:
            try:
                validation = json.loads(response)
            except:
                validation = {"assessment": response}
        
        result = {
            "agent": "QualityValidationAgent",
            "validation": validation,
            "timestamp": datetime.now().isoformat()
        }
        
        self.log_execution({
            "task": target_task,
            "prompt_length": len(prompt)
        }, result)
        
        return result

class AIAgentOrchestrator:
    """Orchestrates multiple AI agents for comprehensive optimization"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.prompt_generator = PromptGenerationAgent(api_key=self.api_key)
        self.result_analyzer = ResultAnalysisAgent(api_key=self.api_key)
        self.adaptive_optimizer = AdaptiveOptimizationAgent(api_key=self.api_key)
        self.quality_validator = QualityValidationAgent(api_key=self.api_key)
        self.execution_log = []
    
    def orchestrate_optimization(
        self,
        initial_prompt: str,
        task_description: str,
        current_iteration: int,
        best_score: float,
        all_results: List[Dict],
        previous_focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate all agents for a complete optimization cycle
        
        Returns:
            Comprehensive optimization plan
        """
        
        # Step 1: Analyze current results
        analysis = self.result_analyzer.execute(all_results, len(all_results), "multi-metric") if all_results else {}
        
        # Step 2: Determine adaptive strategy
        strategy = self.adaptive_optimizer.execute(
            initial_score=0.5,  # Example
            current_best_score=best_score,
            iteration_count=current_iteration,
            previous_focus_areas=previous_focus_areas or []
        )
        
        # Step 3: Extract focus areas from strategy
        focus_areas = strategy.get("strategy", {}).get("focus_areas", ["clarity", "specificity"])
        
        # Step 4: Generate new variations
        new_variations = self.prompt_generator.execute(
            initial_prompt=initial_prompt,
            num_variations=3,
            optimization_focus=focus_areas,
            previous_results=all_results[:5] if all_results else None
        )
        
        # Step 5: Validate quality of best prompt
        best_result = max(all_results, key=lambda x: x.get("score", 0)) if all_results else {}
        validation = self.quality_validator.execute(
            prompt=best_result.get("prompt", initial_prompt),
            target_task=task_description,
            evaluation_results=None
        )
        
        orchestration_result = {
            "orchestration_summary": {
                "iteration": current_iteration,
                "timestamp": datetime.now().isoformat()
            },
            "analysis": analysis,
            "strategy": strategy,
            "new_variations": new_variations,
            "validation": validation
        }
        
        self.execution_log.append(orchestration_result)
        
        return orchestration_result

# Initialize global orchestrator
try:
    AI_ORCHESTRATOR = AIAgentOrchestrator()
except Exception as e:
    logger.error(f"Failed to initialize AI Orchestrator: {e}")
    AI_ORCHESTRATOR = None
