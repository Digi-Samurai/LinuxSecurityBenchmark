import subprocess
import logging

logger = logging.getLogger(__name__)

def check_gdm_removed() -> dict:
    """
    Ensure GDM is removed (Automated)
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.1',
        'name': 'Ensure GDM is removed',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        dpkg_cmd = "dpkg-query -W gdm"
        dpkg_result = subprocess.run(
            dpkg_cmd, shell=True, capture_output=True, text=True
        )

        if dpkg_result.returncode != 0:
            result['status'] = True
            result['details'] = "GDM is not installed"
            logger.info("GDM is not installed")
        else:
            result['status'] = False
            result['details'] = "GDM is installed"
            logger.warning("GDM is installed")

    except Exception as e:
        result['status'] = False
        result['details'] = f"Error checking GDM: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_removed': check_gdm_removed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
