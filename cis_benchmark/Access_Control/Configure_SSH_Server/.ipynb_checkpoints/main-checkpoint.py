import importlib
import logging
import os
import sys
from typing import Dict, Any

# Dynamically determine the project root and add it to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

# Available checks
AVAILABLE_CHECKS = [
    '5_1_1', 
    '5_1_2', 
    '5_1_3', 
    '5_1_4', 
    '5_1_5', 
    '5_1_6', 
    '5_1_7', 
    '5_1_8', 
    '5_1_9', 
    '5_1_10', 
    '5_1_11', 
    '5_1_12', 
    '5_1_13', 
    '5_1_14', 
    '5_1_15', 
    '5_1_16', 
    '5_1_17', 
    '5_1_18', 
    '5_1_19', 
    '5_1_20', 
    '5_1_21', 
    '5_1_22',
]

logger = logging.getLogger(__name__)

def run_all_checks() -> Dict[str, Any]:
    """
    Run all filesystem-related checks
    
    :return: Dictionary of all check results
    """
    results = {}
    
    for check_name in AVAILABLE_CHECKS:
        try:
            # Dynamically import the module using the full path
            module = importlib.import_module(f'cis_benchmark.Access_Control.Configure_SSH_Server.{check_name}')
            
            # Run the checks in the module
            module_results = module.run()
            
            # Merge results
            results.update(module_results)
        
        except ImportError as e:
            logger.error(f"Could not import module {check_name}: {e}")
            # Print additional debug information
            import traceback
            traceback.print_exc()
        except Exception as e:
            logger.error(f"Error running checks for {check_name}: {e}")
            # Print additional debug information
            import traceback
            traceback.print_exc()
    
    return results

def generate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of check results
    
    :param results: Dictionary of check results
    :return: Summary of checks
    """
    summary = {
        'total_checks': 0,
        'passed_checks': 0,
        'failed_checks': 0,
        'compliance_percentage': 0.0
    }
    
    for check_name, check_result in results.items():
        summary['total_checks'] += 1
        
        # Check if the result has a 'status' key
        if isinstance(check_result, dict):
            # Assuming each check has a 'status' key where True means passed
            if check_result.get('status', False):
                summary['passed_checks'] += 1
            else:
                summary['failed_checks'] += 1
    
    # Calculate compliance percentage
    if summary['total_checks'] > 0:
        summary['compliance_percentage'] = (
            summary['passed_checks'] / summary['total_checks'] * 100
        )
    
    return summary

def run():
    """
    Main entry point for filesystem checks
    
    :return: Dictionary containing detailed results and summary
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    
    # Run all checks
    detailed_results = run_all_checks()
    
    # Generate summary
    summary = generate_summary(detailed_results)
    
    # Combine results
    full_results = {
        'detailed_results': detailed_results,
        'summary': summary
    }
    
    return full_results

if __name__ == '__main__':
    # Direct execution for testing
    results = run()
    
    # # Print detailed results
    # print("Detailed Results:")
    # for check, details in results['detailed_results'].items():
    #     print(f"{check}: {details}")
    
    # Print summary
    print("\nSummary:")
    summary = results['summary']
    print(f"Total Checks: {summary['total_checks']}")
    print(f"Passed Checks: {summary['passed_checks']}")
    print(f"Failed Checks: {summary['failed_checks']}")
    print(f"Compliance Percentage: {summary['compliance_percentage']:.2f}%")