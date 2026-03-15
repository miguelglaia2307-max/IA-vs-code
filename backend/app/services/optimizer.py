"""
Prompt Optimization Service

This module implements the core optimization loop:
1. Start with an initial prompt
2. Generate prompt variations
3. Evaluate variations on the dataset
4. Select the best performer
5. Repeat until convergence
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.database_models import (
    OptimizationRun, Program, Metric, Dataset, PromptVariation
)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from difflib import SequenceMatcher
    from collections import Counter
except ImportError:
    pass

class PromptOptimizer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def generate_variations(
        self,
        initial_prompt: str,
        num_variations: int = 5,
        improvement_areas: List[str] = None
    ) -> List[str]:
        """Generate prompt variations using the LLM"""
        
        if not self.client:
            return self._simple_variations(initial_prompt, num_variations)
        
        try:
            areas_text = ""
            if improvement_areas:
                areas_text = f"\nFocus on improving: {', '.join(improvement_areas)}"
            
            system_prompt = """You are an expert prompt engineer. Your task is to generate diverse 
variations of a given prompt that maintain the core meaning but improve clarity, specificity, or formatting.
Generate exactly the requested number of variations. Return ONLY a JSON array of strings, nothing else."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate {num_variations} variations of this prompt:\n\n{initial_prompt}{areas_text}\n\nReturn only JSON array."}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON array from response
            try:
                variations = json.loads(content)
                if isinstance(variations, list):
                    return variations[:num_variations]
            except json.JSONDecodeError:
                # Try to extract array from response if wrapped in text
                match = re.search(r'\[.*\]', content, re.DOTALL)
                if match:
                    try:
                        variations = json.loads(match.group())
                        if isinstance(variations, list):
                            return variations[:num_variations]
                    except json.JSONDecodeError:
                        pass
            
            return self._simple_variations(initial_prompt, num_variations)
        except Exception as e:
            print(f"Error generating variations: {e}")
            return self._simple_variations(initial_prompt, num_variations)
    
    def _simple_variations(self, prompt: str, num_variations: int) -> List[str]:
        """Generate simple variations for when OpenAI is not available"""
        variations = []
        templates = [
            prompt,
            f"Please help me with: {prompt}",
            f"Task: {prompt}",
            f"{prompt}\n\nProvide a detailed and structured response.",
            f"{prompt}\n\nBe specific and concise.",
            f"{prompt}\n\nStep by step:",
            f"Complete this task: {prompt}",
        ]
        return templates[:num_variations]
    
    def evaluate_prompt(
        self,
        prompt: str,
        examples: List[Dict[str, Any]],
        metric_type: str,
        metric_config: Dict[str, Any] = None
    ) -> float:
        """Evaluate a prompt on a dataset"""
        
        if not examples:
            return 0.0
        
        if metric_type == "exact_match":
            return self._evaluate_exact_match(prompt, examples)
        elif metric_type == "similarity":
            return self._evaluate_similarity(prompt, examples)
        elif metric_type == "keyword_match":
            return self._evaluate_keyword_match(prompt, examples)
        elif metric_type == "custom":
            return self._evaluate_custom(prompt, examples, metric_config)
        else:
            return self._evaluate_exact_match(prompt, examples)
    
    def _evaluate_exact_match(self, prompt: str, examples: List[Dict[str, Any]]) -> float:
        """Exact match evaluation - checks if prompt keywords appear in examples"""
        if not examples:
            return 0.0
        
        prompt_lower = prompt.lower()
        words = set(prompt_lower.split())
        
        matches = 0
        for example in examples:
            # Check inputs
            if isinstance(example, dict):
                for value in example.values():
                    if isinstance(value, str):
                        example_words = set(value.lower().split())
                        if words & example_words:  # Intersection
                            matches += 1
                            break
        
        return min(1.0, matches / len(examples)) if examples else 0.0
    
    def _evaluate_similarity(self, prompt: str, examples: List[Dict[str, Any]]) -> float:
        """Similarity-based evaluation using sequence matching"""
        if not examples:
            return 0.0
        
        prompt_lower = prompt.lower()
        similarities = []
        
        for example in examples:
            if isinstance(example, dict):
                for value in example.values():
                    if isinstance(value, str):
                        value_lower = value.lower()
                        ratio = SequenceMatcher(None, prompt_lower, value_lower).ratio()
                        similarities.append(ratio)
        
        if similarities:
            avg_similarity = sum(similarities) / len(similarities)
            return min(1.0, avg_similarity)
        
        return 0.0
    
    def _evaluate_keyword_match(self, prompt: str, examples: List[Dict[str, Any]]) -> float:
        """Keyword matching evaluation"""
        if not examples:
            return 0.0
        
        # Extract keywords (words longer than 4 characters)
        keywords = [word for word in prompt.lower().split() if len(word) > 4]
        if not keywords:
            return 0.5  # Default score if no keywords
        
        matches = 0
        total = 0
        
        for example in examples:
            if isinstance(example, dict):
                example_text = " ".join(str(v).lower() for v in example.values() if v)
                for keyword in keywords:
                    total += 1
                    if keyword in example_text:
                        matches += 1
        
        if total == 0:
            return 0.5
        
        return min(1.0, matches / total)
    
    def _evaluate_custom(
        self,
        prompt: str,
        examples: List[Dict[str, Any]],
        config: Dict[str, Any] = None
    ) -> float:
        """Custom metric evaluation"""
        # Default: combine keyword and similarity metrics
        keyword_score = self._evaluate_keyword_match(prompt, examples)
        similarity_score = self._evaluate_similarity(prompt, examples)
        
        return (keyword_score + similarity_score) / 2
    
    def run_optimization_loop(
        self,
        run_id: int,
        initial_prompt: str,
        num_iterations: int = 5,
        variations_per_iteration: int = 3
    ):
        """Run the full optimization loop"""
        
        db = SessionLocal()
        try:
            run = db.query(OptimizationRun).filter(OptimizationRun.id == run_id).first()
            if not run:
                return
            
            run.status = "running"
            db.commit()
            
            best_prompt = initial_prompt
            best_score = 0.0
            results = []
            
            # Evaluate initial prompt
            program = db.query(Program).filter(Program.id == run.program_id).first()
            metric = db.query(Metric).filter(Metric.id == run.metric_id).first()
            dataset = db.query(Dataset).filter(Dataset.id == run.dataset_id).first()
            
            if not (program and metric and dataset):
                run.status = "failed"
                db.commit()
                return
            
            initial_score = self.evaluate_prompt(
                initial_prompt,
                dataset.examples,
                metric.metric_type,
                metric.config
            )
            best_score = initial_score
            
            for iteration in range(num_iterations):
                # Generate variations
                improvement_areas = ["clarity", "specificity", "structure"] if iteration > 0 else None
                variations = self.generate_variations(best_prompt, variations_per_iteration, improvement_areas)
                
                iteration_results = {
                    "iteration": iteration,
                    "variations": [],
                    "best_in_iteration": None
                }
                
                iteration_best_score = best_score
                iteration_best_prompt = best_prompt
                
                # Evaluate each variation
                for idx, variation in enumerate(variations):
                    score = self.evaluate_prompt(
                        variation,
                        dataset.examples,
                        metric.metric_type,
                        metric.config
                    )
                    
                    # Save variation
                    db_variation = PromptVariation(
                        run_id=run_id,
                        prompt=variation,
                        score=score,
                        iteration=iteration
                    )
                    db.add(db_variation)
                    
                    iteration_results["variations"].append({
                        "index": idx,
                        "prompt": variation[:200] + "..." if len(variation) > 200 else variation,
                        "score": round(score, 4)
                    })
                    
                    # Update best if needed
                    if score > iteration_best_score:
                        iteration_best_score = score
                        iteration_best_prompt = variation
                
                # Update global best
                if iteration_best_score > best_score:
                    best_score = iteration_best_score
                    best_prompt = iteration_best_prompt
                    iteration_results["best_in_iteration"] = best_prompt[:200] + "..." if len(best_prompt) > 200 else best_prompt
                
                iteration_results["best_score"] = round(best_score, 4)
                results.append(iteration_results)
                
                run.iterations = iteration + 1
                run.best_prompt = best_prompt
                run.best_score = best_score
                run.results = results
                db.commit()
            
            run.status = "completed"
            db.commit()
        
        except Exception as e:
            run.status = "failed"
            db.commit()
            print(f"Optimization error: {e}")
        finally:
            db.close()

async def run_optimization_async(
    run_id: int,
    program_id: int,
    metric_id: int,
    dataset_id: int
):
    """Async task for running optimization"""
    
    db = SessionLocal()
    try:
        run = db.query(OptimizationRun).filter(OptimizationRun.id == run_id).first()
        if run:
            optimizer = PromptOptimizer()
            optimizer.run_optimization_loop(
                run_id=run_id,
                initial_prompt=run.initial_prompt,
                num_iterations=5,
                variations_per_iteration=3
            )
    finally:
        db.close()

