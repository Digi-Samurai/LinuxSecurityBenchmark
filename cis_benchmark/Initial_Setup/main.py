import os
import sys
import importlib
import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    format='%(levelname)s:%(name)s:%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dynamically determine the root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

# Define compliance categories
CATEGORIES = [
    "Filesystem",
    "Package_Management",
    "Mandatory_Access_Control",
    "Configure_Bootloader",
    "Configure_Additional_Process_Hardening",
    "Configure_Command_Line_Warnin_Banners",
    "Configure_GNOME_Display_Manager"
]

def run_checks() -> Dict[str, Any]:
    """Runs all compliance checks across all categories and aggregates results."""
    results = {}
    total_summary = {
        "total_checks": 0,
        "passed_checks": 0,
        "failed_checks": 0,
    }

    for category in CATEGORIES:
        category_path = os.path.join(ROOT_DIR, category)
        main_script = os.path.join(category_path, "main.py")

        if os.path.exists(main_script):
            try:
                print(f"\n=== Running checks for {category}... ===")

                # Dynamically import and run category main.py
                module_name = f"{category}.main".replace("/", ".")
                category_module = importlib.import_module(module_name)

                if hasattr(category_module, "run"):
                    category_results = category_module.run()
                    
                    # Store detailed results
                    results[category] = category_results["detailed_results"]
                    
                    # Update summary stats
                    total_summary["total_checks"] += category_results["summary"]["total_checks"]
                    total_summary["passed_checks"] += category_results["summary"]["passed_checks"]
                    total_summary["failed_checks"] += category_results["summary"]["failed_checks"]

                else:
                    logger.error(f"run() missing in {category}.main.py")

            except Exception as e:
                logger.error(f"Error running {category}: {str(e)}")

    # Calculate compliance percentage
    if total_summary["total_checks"] > 0:
        total_summary["compliance_percentage"] = (
            total_summary["passed_checks"] / total_summary["total_checks"] * 100
        )
    else:
        total_summary["compliance_percentage"] = 0.0

    return {"detailed_results": results, "summary": total_summary}

if __name__ == "__main__":
    compliance_results = run_checks()
    
    # Print final summary
    print("\n=== Compliance Summary ===")
    summary = compliance_results["summary"]
    print(f"Total Checks: {summary['total_checks']}")
    print(f"Passed Checks: {summary['passed_checks']}")
    print(f"Failed Checks: {summary['failed_checks']}")
    print(f"Compliance Percentage: {summary['compliance_percentage']:.2f}%")
    
    logger.info("Compliance Check Completed.")
