import os
import sys
import importlib
import logging
from typing import Dict, Any
from termcolor import colored
from rich.console import Console
from rich.table import Table

console = Console()


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
    "Initial_Setup",
    "Services",
    "Network",
    "Host_Based_Firewall",
    "Access_Control",
    "Logging_and_Auditing",
    "System_Maintenance"
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
                print(colored(f"\n=== Running checks for {category} ===","green"))

                # Dynamically import and run category main.py
                module_name = f"{category}.main".replace("/", ".")
                category_module = importlib.import_module(module_name)

                if hasattr(category_module, "run_checks"):
                    category_results = category_module.run_checks()
                    
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


def display_results(results: Dict[str, Any]):
    """Display results in a tabular format using rich."""
    
    # Iterate over categories and their respective checks
    for category, checks in results['detailed_results'].items():
        console.print(f"\n[bold green]Category: {category}[/bold green]")

        # Create a new table for each category
        table = Table(title=f"Compliance Checks for {category}", show_header=True, header_style="bold cyan")

        # Add columns for the table
        table.add_column("Check", style="dim")
        table.add_column("Benchmark ID")
        table.add_column("Name")
        table.add_column("Status")
        table.add_column("Severity")
        table.add_column("Details")
        
        # Iterate over each check within the category
        for check_name, check_details in checks.items():
            # Print the name of the sub-check (e.g., cramfs_module)
            console.print(f"\n[bold cyan]{check_name}[/bold cyan]")

            # Iterate over the details of the sub-checks
            for sub_check_name, sub_check_details in check_details.items():
                # Extract necessary details
                benchmark_id = sub_check_details.get('benchmark_id', 'N/A')
                name = sub_check_details.get('name', 'N/A')
                status = "Passed" if sub_check_details.get('status', False) else "Failed"
                severity = sub_check_details.get('severity', 'N/A')
                details = sub_check_details.get('details', 'N/A')

                # Add the row to the table for this sub-check
                table.add_row(
                    sub_check_name,  # This is the sub-check name (e.g., cramfs_module)
                    benchmark_id,
                    name,
                    status,
                    severity,
                    details
                )

        # Print the table for this category
        console.print(table)

def main():
    compliance_results = run_checks()

    print("\n=== Benchmark results ===")
    # Display detailed results in a tabular format
    display_results(compliance_results)
    
    # Print final summary
    print("\n=== Compliance Summary ===")
    summary = compliance_results["summary"]
    print(f"Total Checks: {summary['total_checks']}")
    print(f"Passed Checks: {summary['passed_checks']}")
    print(f"Failed Checks: {summary['failed_checks']}")
    print(f"Compliance Percentage: {summary['compliance_percentage']:.2f}%")
    
    logger.info("Compliance Check Completed.")

if __name__ == "__main__":
    main()