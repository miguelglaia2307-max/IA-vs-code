"""
Script to seed the database with test data for development
Run this after setting up the backend to populate initial test data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models.database_models import (
    Project, Signature, Dataset, Metric, Program
)

def seed_database():
    """Seed the database with test data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_project = db.query(Project).first()
        if existing_project:
            print("Database already seeded. Skipping...")
            return
        
        # Create a test project
        project = Project(
            name="Customer Service Optimization",
            description="Optimize prompts for customer service AI assistant"
        )
        db.add(project)
        db.flush()
        
        # Create a signature
        signature = Signature(
            project_id=project.id,
            name="Customer Support",
            description="Customer support query and response",
            input_fields=[
                {"name": "customer_message", "type": "string", "description": "The customer's question or complaint"},
                {"name": "context", "type": "string", "description": "Previous conversation context"}
            ],
            output_fields=[
                {"name": "response", "type": "string", "description": "The support agent's response"},
                {"name": "sentiment", "type": "string", "description": "Sentiment of the response (positive, neutral, negative)"}
            ]
        )
        db.add(signature)
        db.flush()
        
        # Create a dataset
        dataset = Dataset(
            project_id=project.id,
            signature_id=signature.id,
            name="Support Tickets",
            examples=[
                {
                    "input": "My order hasn't arrived in 2 weeks!",
                    "expected_output": "I sincerely apologize for the delay. Let me investigate this right away."
                },
                {
                    "input": "How do I reset my password?",
                    "expected_output": "You can reset your password by clicking 'Forgot Password' on the login page."
                },
                {
                    "input": "Your product broke after one day!",
                    "expected_output": "I'm sorry to hear that. We'll replace it immediately at no cost."
                },
                {
                    "input": "Can I return my purchase?",
                    "expected_output": "Yes, we offer a 30-day return policy. Let me help you with that."
                },
                {
                    "input": "When is your next sale?",
                    "expected_output": "Our next sale is coming up next month. Subscribe to our newsletter for early access."
                }
            ]
        )
        db.add(dataset)
        db.flush()
        
        # Create a metric
        metric = Metric(
            project_id=project.id,
            signature_id=signature.id,
            name="Response Quality",
            metric_type="keyword_match",
            config={"keywords": ["sincerely", "apologize", "help", "please"]}
        )
        db.add(metric)
        db.flush()
        
        # Create a program
        program = Program(
            project_id=project.id,
            signature_id=signature.id,
            name="Support Response Generator",
            description="Generate empathetic customer support responses",
            code="""
def generate_response(customer_message, context):
    # This is where the LLM would process the customer message
    # and generate an appropriate response
    pass
"""
        )
        db.add(program)
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   - Created 1 project: {project.name}")
        print(f"   - Created 1 signature: {signature.name}")
        print(f"   - Created 1 dataset with {len(dataset.examples)} examples")
        print(f"   - Created 1 metric: {metric.name}")
        print(f"   - Created 1 program: {program.name}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
