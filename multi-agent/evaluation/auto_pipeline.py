#!/usr/bin/env python3
"""
Multi-Agent Knowledge Graph Evaluation Pipeline
===============================================

Pipeline tự động để đánh giá hệ thống đồ thị tri thức đa tác nhân.
Bao gồm các bước: Phân tích đồ thị, Trích xuất câu trả lời, Đánh giá, Visualization.

Author: Multi-Agent Evaluation System
Date: June 2025
"""

import os
import sys
import time
import asyncio
import logging
import traceback
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Setup logging
def setup_logging():
    """Thiết lập logging cho pipeline"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/evaluation_pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class EvaluationPipeline:
    """
    Pipeline tự động cho việc đánh giá hệ thống đồ thị tri thức đa tác nhân
    """
    
    def __init__(self, config: Dict = None):
        """Khởi tạo pipeline"""
        self.start_time = time.time()
        self.config = config or self._load_default_config()
        self.results_dir = Path("evaluation_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Các file output chính
        self.output_files = {
            'graph_analysis': 'graph_analysis_from_neo4j.csv',
            'answers': 'evaluation_answers_only.xlsx', 
            'concepts': 'evaluation_kg_concepts.xlsx',
            'labels': 'evaluation_labels_only.xlsx',
            'concept_results': 'evaluation_concepts_result.xlsx',
            'charts_dir': 'evaluation_charts',
            'summary_report': 'evaluation_summary_report.md'
        }
        
        logger.info("🚀 Khởi tạo Evaluation Pipeline")
        logger.info(f"📁 Thư mục kết quả: {self.results_dir}")

    def _load_default_config(self) -> Dict:
        """Load cấu hình mặc định"""
        return {
            'neo4j': {
                'uri': os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
                'user': os.getenv('NEO4J_USER', 'neo4j'),
                'password': os.getenv('NEO4J_PASSWORD', 'password'),
                'databases': ['deepseek', 'gemini', 'openai']
            },
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': 'gpt-4o-mini'
            },
            'evaluation': {
                'similarity_threshold': 0.6,
                'search_limit': 30,
                'score_threshold': 6
            }
        }

    def check_prerequisites(self) -> bool:
        """Kiểm tra điều kiện tiên quyết"""
        logger.info("🔍 Kiểm tra điều kiện tiên quyết...")
        
        # Check dependencies
        required_modules = ['pandas', 'numpy', 'matplotlib', 'networkx', 'neo4j', 'openai', 'dotenv']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module.replace('-', '_'))
                logger.info(f"✅ {module}")
            except ImportError:
                missing_modules.append(module)
                logger.error(f"❌ {module}")
        
        if missing_modules:
            logger.error(f"Thiếu modules: {missing_modules}")
            return False
        
        # Check required files
        required_files = [
            'evalute_graph.py',
            'extract_answers.py', 
            'extract_concept_file.py',
            'llm_evaluate.py',
            'visualization.py',
            'sgu_golden_answers_updated.csv'
        ]
        
        missing_files = []
        for file_name in required_files:
            if not Path(file_name).exists():
                missing_files.append(file_name)
                logger.error(f"❌ {file_name}")
            else:
                logger.info(f"✅ {file_name}")
        
        if missing_files:
            logger.error(f"Thiếu files: {missing_files}")
            return False
        
        # Check environment
        if not self.config['openai']['api_key'] or self.config['openai']['api_key'] == 'your_openai_api_key_here':
            logger.error("❌ OpenAI API key chưa được cấu hình")
            return False
        
        logger.info("✅ Tất cả điều kiện tiên quyết đã đủ")
        return True

    async def run_phase_1_graph_analysis(self) -> bool:
        """Phase 1: Phân tích đồ thị từ Neo4j"""
        logger.info("📊 Phase 1: Phân tích đồ thị...")
        
        try:
            # Import và chạy graph analysis
            from evalute_graph import main_analysis
            
            logger.info("Chạy phân tích đồ thị từ Neo4j...")
            await asyncio.to_thread(main_analysis)
            
            # Kiểm tra output
            output_file = self.output_files['graph_analysis']
            if Path(output_file).exists():
                logger.info(f"✅ Đã tạo: {output_file}")
                return True
            else:
                logger.error(f"❌ Không tìm thấy output: {output_file}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Lỗi trong Phase 1: {e}")
            traceback.print_exc()
            return False

    async def run_phase_2_extract_answers(self) -> bool:
        """Phase 2: Trích xuất câu trả lời từ các models"""
        logger.info("💬 Phase 2: Trích xuất câu trả lời...")
        
        try:
            # Import và chạy extract answers
            from extract_answers import main_async
            
            logger.info("Trích xuất câu trả lời từ 3 models...")
            await main_async()
            
            # Kiểm tra output
            output_file = self.output_files['answers']
            if Path(output_file).exists():
                logger.info(f"✅ Đã tạo: {output_file}")
                return True
            else:
                logger.error(f"❌ Không tìm thấy output: {output_file}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Lỗi trong Phase 2: {e}")
            traceback.print_exc()
            return False

    async def run_phase_3_extract_concepts(self) -> bool:
        """Phase 3: Trích xuất concepts từ đáp án chuẩn"""
        logger.info("🧠 Phase 3: Trích xuất concepts...")
        
        try:
            # Import và chạy concept extraction
            import extract_concept_file
            
            logger.info("Trích xuất concepts từ đáp án chuẩn...")
            await asyncio.to_thread(lambda: exec(open('extract_concept_file.py').read()))
            
            # Kiểm tra output
            output_file = self.output_files['concepts']
            if Path(output_file).exists():
                logger.info(f"✅ Đã tạo: {output_file}")
                return True
            else:
                logger.error(f"❌ Không tìm thấy output: {output_file}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Lỗi trong Phase 3: {e}")
            traceback.print_exc()
            return False

    async def run_phase_4_evaluation(self) -> bool:
        """Phase 4: Đánh giá và chấm điểm"""
        logger.info("🎯 Phase 4: Đánh giá và chấm điểm...")
        
        try:
            # Kiểm tra input files
            if not Path(self.output_files['answers']).exists():
                logger.error("❌ Thiếu file answers. Chạy Phase 2 trước.")
                return False
            
            if not Path(self.output_files['concepts']).exists():
                logger.error("❌ Thiếu file concepts. Chạy Phase 3 trước.")
                return False
            
            # Import và chạy evaluation
            from llm_evaluate import evaluate_from_file
            
            logger.info("Đánh giá câu trả lời và concepts...")
            await asyncio.to_thread(
                evaluate_from_file, 
                self.output_files['answers'], 
                self.output_files['concepts']
            )
            
            # Kiểm tra outputs
            if Path(self.output_files['labels']).exists() and Path(self.output_files['concept_results']).exists():
                logger.info(f"✅ Đã tạo files đánh giá")
                return True
            else:
                logger.error(f"❌ Không tìm thấy output files đánh giá")
                return False
                
        except Exception as e:
            logger.error(f"❌ Lỗi trong Phase 4: {e}")
            traceback.print_exc()
            return False

    async def run_phase_5_visualization(self) -> bool:
        """Phase 5: Tạo visualization và charts"""
        logger.info("📈 Phase 5: Tạo visualization...")
        
        try:
            # Kiểm tra input files
            if not Path(self.output_files['labels']).exists():
                logger.error("❌ Thiếu file labels. Chạy Phase 4 trước.")
                return False
            
            if not Path(self.output_files['concept_results']).exists():
                logger.error("❌ Thiếu file concept results. Chạy Phase 4 trước.")
                return False
            
            # Import và chạy visualization
            from visualization import create_all_visualizations
            
            logger.info("Tạo charts và visualization...")
            charts = await asyncio.to_thread(
                create_all_visualizations,
                self.output_files['labels'],
                self.output_files['concept_results'],
                self.output_files['charts_dir']
            )
            
            if charts:
                logger.info(f"✅ Đã tạo {len(charts)} charts")
                return True
            else:
                logger.error("❌ Không tạo được charts")
                return False
                
        except Exception as e:
            logger.error(f"❌ Lỗi trong Phase 5: {e}")
            traceback.print_exc()
            return False

    def generate_summary_report(self) -> bool:
        """Tạo báo cáo tổng hợp"""
        logger.info("📋 Tạo báo cáo tổng hợp...")
        
        try:
            report_path = self.output_files['summary_report']
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"""# Evaluation Summary Report
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Pipeline Runtime: {time.time() - self.start_time:.2f} seconds

            ## Files Generated
            """)
                
                for name, filename in self.output_files.items():
                    if name != 'summary_report':
                        file_path = Path(filename)
                        if file_path.exists():
                            if file_path.is_file():
                                size = file_path.stat().st_size
                                f.write(f"- ✅ {name}: `{filename}` ({size:,} bytes)\n")
                            else:
                                files = list(file_path.glob("*"))
                                f.write(f"- ✅ {name}: `{filename}` ({len(files)} files)\n")
                        else:
                            f.write(f"- ❌ {name}: `{filename}` (missing)\n")
                
                # Load và hiển thị kết quả đánh giá
                if Path(self.output_files['labels']).exists():
                    df_labels = pd.read_excel(self.output_files['labels'])
                    f.write(f"\n## Evaluation Results\n")
                    f.write(f"- Total Questions: {len(df_labels)}\n")
                    
                    for model in ['DeepSeek', 'Gemini', 'OpenAI']:
                        if f'Label_{model}' in df_labels.columns:
                            counts = df_labels[f'Label_{model}'].value_counts()
                            f.write(f"- {model}: Right={counts.get('Right', 0)}, Partial={counts.get('Partial', 0)}, Wrong={counts.get('Wrong', 0)}\n")
                
                f.write(f"\n## Configuration Used\n")
                f.write(f"```json\n{self.config}\n```\n")
            
            logger.info(f"✅ Đã tạo báo cáo: {report_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Lỗi tạo báo cáo: {e}")
            return False

    async def run_full_pipeline(self) -> bool:
        """Chạy toàn bộ pipeline"""
        logger.info("🚀 Bắt đầu chạy toàn bộ Evaluation Pipeline")
        
        # Check prerequisites
        if not self.check_prerequisites():
            logger.error("❌ Điều kiện tiên quyết không đủ")
            return False
        
        # Run các phases
        phases = [
            ("Phase 1: Graph Analysis", self.run_phase_1_graph_analysis),
            ("Phase 2: Extract Answers", self.run_phase_2_extract_answers), 
            ("Phase 3: Extract Concepts", self.run_phase_3_extract_concepts),
            ("Phase 4: Evaluation", self.run_phase_4_evaluation),
            ("Phase 5: Visualization", self.run_phase_5_visualization)
        ]
        
        results = {}
        for phase_name, phase_func in phases:
            logger.info(f"\n{'='*50}")
            logger.info(f"🔄 Bắt đầu {phase_name}")
            
            start_time = time.time()
            success = await phase_func()
            duration = time.time() - start_time
            
            results[phase_name] = {
                'success': success,
                'duration': duration
            }
            
            if success:
                logger.info(f"✅ {phase_name} hoàn thành ({duration:.2f}s)")
            else:
                logger.error(f"❌ {phase_name} thất bại ({duration:.2f}s)")
                break
        
        # Generate summary report
        self.generate_summary_report()
        
        # Final summary
        total_time = time.time() - self.start_time
        successful_phases = sum(1 for r in results.values() if r['success'])
        total_phases = len(phases)
        
        logger.info(f"\n{'='*50}")
        logger.info(f"🎯 Pipeline hoàn thành!")
        logger.info(f"✅ Thành công: {successful_phases}/{total_phases} phases")
        logger.info(f"⏱️ Tổng thời gian: {total_time:.2f} seconds")
        logger.info(f"📋 Báo cáo: {self.output_files['summary_report']}")
        
        return successful_phases == total_phases

async def main():
    """Main function"""
    pipeline = EvaluationPipeline()
    success = await pipeline.run_full_pipeline()
    
    if success:
        print("\n🎉 Pipeline hoàn thành thành công!")
        print("📁 Kiểm tra thư mục evaluation_results/ để xem kết quả")
    else:
        print("\n❌ Pipeline thất bại hoặc không hoàn thành")
        print("📋 Kiểm tra logs để xem chi tiết lỗi")

if __name__ == "__main__":
    asyncio.run(main())
