import os
import logging

logger = logging.getLogger(__name__)

GDM_XDMCP_CONFIG = "/etc/gdm/custom.conf"

def check_xdmcp_disabled() -> dict:
    """
    Ensure XDMCP is disabled in GDM settings.
    CIS Benchmark 1.7.10 - Ensure XDMCP is not enabled.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.10',
        'name': 'Ensure XDMCP is not enabled',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        if os.path.exists(GDM_XDMCP_CONFIG):
            with open(GDM_XDMCP_CONFIG, 'r') as f:
                content = f.read()
                if "[xdmcp]" in content and "Enable=true" in content:
                    result['details'] = "XDMCP is enabled, which is a security risk."
                    logger.warning(result['details'])
                else:
                    result['status'] = True
                    result['details'] = "XDMCP is correctly disabled."
                    logger.info(result['details'])
        else:
            result['details'] = f"{GDM_XDMCP_CONFIG} not found, XDMCP might be disabled by default."
            logger.info(result['details'])

    except Exception as e:
        result['details'] = f"Error checking XDMCP setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'xdmcp_disabled': check_xdmcp_disabled()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
