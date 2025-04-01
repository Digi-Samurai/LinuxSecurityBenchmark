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
    '6_2_1_1',
    '6_2_1_2',
    '6_2_1_3',
    '6_2_1_4',
    '6_2_2_1',
    '6_2_2_2',
    '6_2_2_3',
    '6_2_2_4',
    '6_2_3_1',
    '6_2_3_2',
    '6_2_3_3',
    '6_2_3_4',
    '6_2_3_5',
    '6_2_3_6',
    '6_2_3_7',
    '6_2_3_8',
    '6_2_3_9',
    '6_2_3_10',
    '6_2_3_11',
    '6_2_3_12',
    '6_2_3_13',
    '6_2_3_14',
    '6_2_3_15',
    '6_2_3_16',
    '6_2_3_17',
    '6_2_3_18',
    '6_2_3_19',
    '6_2_3_20',
    '6_2_4_1', 
    '6_2_4_2', 
    '6_2_4_3', 
    '6_2_4_4', 
    '6_2_4_5', 
    '6_2_4_6', 
    '6_2_4_7', 
    '6_2_4_8',
    '6_2_4_9',
    '6_2_4_10',
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
            module = importlib.import_module(f'cis_benchmark.Logging_and_Auditing.System_Auditing.{check_name}')
            
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