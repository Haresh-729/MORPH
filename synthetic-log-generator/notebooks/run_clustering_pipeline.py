#!/usr/bin/env python3
"""
Quick script to run the complete few-shot clustering pipeline.

This script executes all notebooks in sequence:
1. Data Exploration
2. Feature Engineering
3. Few-Shot Clustering
4. Evaluation and Analysis

Usage:
    python run_clustering_pipeline.py
    python run_clustering_pipeline.py --notebooks 3,4  # Run only specific notebooks
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{BLUE}ℹ️  {text}{RESET}")

def check_prerequisites():
    """Check if required files and packages exist."""
    print_header("Checking Prerequisites")
    
    issues = []
    
    # Check if logs exist
    log_file = Path("../output/grafana/logs_2024-01-01.jsonl")
    if not log_file.exists():
        issues.append(f"Log file not found: {log_file}")
        print_error(f"Log file not found: {log_file}")
    else:
        print_success(f"Found log file: {log_file}")
    
    # Check if required packages are installed
    required_packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'hdbscan',
        'sentence_transformers',
        'faiss',
        'umap'
    ]
    
    print_info("Checking required packages...")
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"  {package}")
        except ImportError:
            missing_packages.append(package)
            print_error(f"  {package}")
    
    if missing_packages:
        issues.append(f"Missing packages: {', '.join(missing_packages)}")
        print_warning(f"\nInstall missing packages with:")
        print(f"  pip install -r requirements_notebooks.txt")
    
    return len(issues) == 0, issues

def run_notebook(notebook_path, notebook_name):
    """Execute a Jupyter notebook using papermill."""
    print_header(f"Running: {notebook_name}")
    
    output_path = notebook_path.replace('.ipynb', '_executed.ipynb')
    
    try:
        # Try using papermill if available
        try:
            import papermill as pm
            print_info(f"Executing with papermill: {notebook_path}")
            start_time = time.time()
            
            pm.execute_notebook(
                notebook_path,
                output_path,
                kernel_name='python3'
            )
            
            elapsed = time.time() - start_time
            print_success(f"Completed in {elapsed:.1f} seconds")
            return True
            
        except ImportError:
            # Fallback to nbconvert
            print_warning("papermill not found, using nbconvert...")
            cmd = [
                'jupyter', 'nbconvert',
                '--to', 'notebook',
                '--execute',
                '--output', output_path,
                notebook_path
            ]
            
            start_time = time.time()
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            elapsed = time.time() - start_time
            
            print_success(f"Completed in {elapsed:.1f} seconds")
            return True
            
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to execute notebook: {e}")
        if e.stderr:
            print(f"\nError output:\n{e.stderr}")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Main pipeline execution."""
    print_header("MOZAIC Few-Shot Clustering Pipeline")
    print_info("This will execute all clustering notebooks in sequence.")
    print()
    
    # Check prerequisites
    prereqs_ok, issues = check_prerequisites()
    if not prereqs_ok:
        print_error("Prerequisites check failed!")
        print("\nIssues found:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    
    print_success("All prerequisites satisfied!\n")
    
    # Define notebooks to run
    notebooks = [
        ("1_data_exploration.ipynb", "Data Exploration"),
        ("2_feature_engineering.ipynb", "Feature Engineering"),
        ("3_fewshot_clustering.ipynb", "Few-Shot Clustering"),
        ("4_evaluation_and_analysis.ipynb", "Evaluation and Analysis")
    ]
    
    # Parse command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--notebooks':
        if len(sys.argv) > 2:
            selected = [int(x) - 1 for x in sys.argv[2].split(',')]
            notebooks = [notebooks[i] for i in selected if 0 <= i < len(notebooks)]
            print_info(f"Running selected notebooks: {[n[1] for n in notebooks]}\n")
    
    # Execute notebooks
    start_time = time.time()
    results = []
    
    for i, (notebook_file, notebook_name) in enumerate(notebooks, 1):
        print(f"\n{BOLD}Step {i}/{len(notebooks)}{RESET}")
        success = run_notebook(notebook_file, notebook_name)
        results.append((notebook_name, success))
        
        if not success:
            print_error(f"Failed to execute {notebook_name}")
            print_warning("Stopping pipeline execution.")
            break
        
        # Small delay between notebooks
        if i < len(notebooks):
            time.sleep(2)
    
    # Summary
    total_time = time.time() - start_time
    print_header("Pipeline Execution Summary")
    
    print(f"\n{BOLD}Results:{RESET}")
    all_success = True
    for name, success in results:
        if success:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
            all_success = False
    
    print(f"\n{BOLD}Total Time:{RESET} {total_time/60:.1f} minutes")
    
    if all_success:
        print_success("\n🎉 All notebooks executed successfully!")
        print_info("\nGenerated outputs in: output/grafana/")
        print_info("  - clustered_logs.parquet")
        print_info("  - embeddings.npy")
        print_info("  - faiss_index.bin")
        print_info("  - evaluation_report.json")
        print_info("  - Multiple visualization PNGs")
        return 0
    else:
        print_error("\n❌ Some notebooks failed to execute.")
        print_warning("Check the error messages above for details.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_warning("\n\nPipeline interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
