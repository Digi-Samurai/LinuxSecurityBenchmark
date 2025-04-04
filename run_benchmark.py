import os
import sys
import importlib
from typing import Dict, Any
from termcolor import colored
from rich.console import Console
from rich.table import Table

console = Console()

# Dynamically determine the root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

# Path to cis_benchmark module
CIS_BENCHMARK_MODULE = "cis_benchmark.main"

def run_benchmark():
    """Dynamically imports and runs the `run_checks()` function from cis_benchmark.main."""
    try:
        # Dynamically import the `main` module from `cis_benchmark`
        category_module = importlib.import_module(CIS_BENCHMARK_MODULE)

        # Ensure the `run_checks()` function exists in the module
        if hasattr(category_module, "run_checks"):
            # Call the run_checks function from the imported module
            results = category_module.run_checks()

            # Return the results
            return results

        else:
            print("run_checks() function is missing in cis_benchmark.main.")
            return None

    except Exception as e:
        print(f"An error occurred while running the benchmark: {str(e)}")
        return None

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

if __name__ == "__main__":
    # Run the benchmark
    benchmark_results = run_benchmark()

    if benchmark_results:
        print("Benchmark results:")
        # Display detailed results in a tabular format
        display_results(benchmark_results)
    else:
        print("No results returned from the benchmark.")

