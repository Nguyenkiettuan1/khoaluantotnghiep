#!/usr/bin/env python3
"""
Multi-Agent Ontology Generation System
Main orchestration script for running the complete workflow
"""

import os
import asyncio
import argparse
from pathlib import Path
from datetime import datetime
import logging

# Import các modules
from generate_cqs import main as generate_cqs_main
from generate_skeleton_ontology import generate_ontology_from_cqs
from generate_ontology_parallel import main as generate_parallel_main
from import_to_neo4j import main as import_neo4j_main

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/main_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OntologyWorkflow:
    """Main workflow orchestrator for ontology generation system"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            "CQs", "ontology", "cypher_deepseek_sguv1", 
            "cypher_gemini_sguv2", "cypher_openai_sguv3", "logs"
        ]
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
    
    async def step1_generate_competency_questions(self, num_questions=40):
        """Step 1: Generate Competency Questions from dataset"""
        logger.info("=== STEP 1: Generating Competency Questions ===")
        try:
            generate_cqs_main(num_questions)
            logger.info("✅ Competency questions generated successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to generate competency questions: {str(e)}")
            return False
    
    def step2_generate_skeleton_ontology(self):
        """Step 2: Generate skeleton ontology from CQs"""
        logger.info("=== STEP 2: Generating Skeleton Ontology ===")
        try:
            generate_ontology_from_cqs(
                qc_folder="CQs",
                output_path="./ontology/skeleton_ontology.ttl",
                model="gpt-4o-mini"
            )
            logger.info("✅ Skeleton ontology generated successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to generate skeleton ontology: {str(e)}")
            return False
    
    async def step3_generate_cypher_parallel(self):
        """Step 3: Generate Cypher queries using multiple LLM models in parallel"""
        logger.info("=== STEP 3: Generating Cypher with Multiple Models ===")
        try:
            await generate_parallel_main()
            logger.info("✅ Cypher generation completed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to generate Cypher: {str(e)}")
            return False
    
    def step4_import_to_neo4j(self):
        """Step 4: Import generated Cypher to Neo4j databases"""
        logger.info("=== STEP 4: Importing to Neo4j Databases ===")
        try:
            import_neo4j_main()
            logger.info("✅ Data imported to Neo4j successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to import to Neo4j: {str(e)}")
            return False
    
    async def run_complete_workflow(self, num_questions=40, skip_steps=None):
        """Run the complete workflow"""
        skip_steps = skip_steps or []
        logger.info("🚀 Starting Complete Ontology Generation Workflow")
        
        start_time = datetime.now()
        results = {}
        
        # Step 1: Generate CQs
        if 1 not in skip_steps:
            results['step1'] = await self.step1_generate_competency_questions(num_questions)
        else:
            logger.info("⏭️ Skipping Step 1: Generate Competency Questions")
            results['step1'] = True
        
        # Step 2: Generate skeleton ontology
        if 2 not in skip_steps and results.get('step1', True):
            results['step2'] = self.step2_generate_skeleton_ontology()
        else:
            if 2 in skip_steps:
                logger.info("⏭️ Skipping Step 2: Generate Skeleton Ontology")
                results['step2'] = True
            else:
                logger.error("❌ Skipping Step 2 due to Step 1 failure")
                results['step2'] = False
        
        # Step 3: Generate Cypher in parallel
        if 3 not in skip_steps and results.get('step2', True):
            results['step3'] = await self.step3_generate_cypher_parallel()
        else:
            if 3 in skip_steps:
                logger.info("⏭️ Skipping Step 3: Generate Cypher")
                results['step3'] = True
            else:
                logger.error("❌ Skipping Step 3 due to previous failures")
                results['step3'] = False
        
        # Step 4: Import to Neo4j
        if 4 not in skip_steps and results.get('step3', True):
            results['step4'] = self.step4_import_to_neo4j()
        else:
            if 4 in skip_steps:
                logger.info("⏭️ Skipping Step 4: Import to Neo4j")
                results['step4'] = True
            else:
                logger.error("❌ Skipping Step 4 due to previous failures")
                results['step4'] = False
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("=" * 60)
        logger.info("📊 WORKFLOW SUMMARY")
        logger.info("=" * 60)
        logger.info(f"⏱️ Total execution time: {duration}")
        logger.info(f"📋 Step 1 - Generate CQs: {'✅ SUCCESS' if results.get('step1') else '❌ FAILED'}")
        logger.info(f"🔗 Step 2 - Generate Ontology: {'✅ SUCCESS' if results.get('step2') else '❌ FAILED'}")
        logger.info(f"🤖 Step 3 - Generate Cypher: {'✅ SUCCESS' if results.get('step3') else '❌ FAILED'}")
        logger.info(f"💾 Step 4 - Import to Neo4j: {'✅ SUCCESS' if results.get('step4') else '❌ FAILED'}")
        
        success_count = sum(1 for v in results.values() if v)
        logger.info(f"🎯 Overall Success Rate: {success_count}/{len(results)} steps completed")
        
        return all(results.values())

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Multi-Agent Ontology Generation System")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4], 
                       help="Run only specific step (1-4)")
    parser.add_argument("--skip", type=int, nargs='+', choices=[1, 2, 3, 4],
                       help="Skip specific steps")
    parser.add_argument("--questions", type=int, default=40,
                       help="Number of competency questions to generate")
    parser.add_argument("--complete", action="store_true",
                       help="Run complete workflow")
    
    args = parser.parse_args()
    
    # Create workflow instance
    workflow = OntologyWorkflow()
    
    async def run_workflow():
        if args.step:
            # Run specific step
            if args.step == 1:
                await workflow.step1_generate_competency_questions(args.questions)
            elif args.step == 2:
                workflow.step2_generate_skeleton_ontology()
            elif args.step == 3:
                await workflow.step3_generate_cypher_parallel()
            elif args.step == 4:
                workflow.step4_import_to_neo4j()
        elif args.complete or not any([args.step, args.skip]):
            # Run complete workflow
            await workflow.run_complete_workflow(
                num_questions=args.questions,
                skip_steps=args.skip
            )
        else:
            # Run workflow with skipped steps
            await workflow.run_complete_workflow(
                num_questions=args.questions,
                skip_steps=args.skip
            )
    
    # Run the workflow
    asyncio.run(run_workflow())

if __name__ == "__main__":
    main()
