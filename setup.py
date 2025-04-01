```python
from setuptools import setup, find_packages

setup(
    name='cis_benchmark_tool',
    version='2.0.0',
    description='Comprehensive CIS Benchmark Security Auditing Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Xhunter',
    url='https://github.com/xhunter101/cis-benchmark-tool',
    packages=find_packages(),
    install_requires=[
        'termcolor>=1.1.0',
        'colorama>=0.4.4',
        'psutil>=5.8.0',
    ],
    entry_points={
        'console_scripts': [
            'cis-benchmark=cis_benchmark.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Security',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.8',
    keywords='security benchmark cis linux audit',
)
```
