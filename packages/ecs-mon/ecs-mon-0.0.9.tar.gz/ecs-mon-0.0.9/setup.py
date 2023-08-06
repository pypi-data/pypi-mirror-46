import sys
import os
import re
from setuptools import setup, find_packages


requires = [
    'boto3>=1.7.20, <2.0',
    'botocore>=1.10.20, <2.0',
    'prettytable>=0.7.2, <1.0.0'
]

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'ecs_mon', 'version.py'), 'r') as f:
    exec(f.read(), about)

# Get the long description from the relevant file
try:
    # in addition to pip install pypandoc, might have to: apt install -y pandoc
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (OSError, IOError, ImportError) as e:
    print("Error converting README.md to rst:", str(e))
    long_description = open('README.md').read()

setup(name=about['__title__'],
      version=about['__version__'],
      description=about['__description__'],
      long_description=long_description,
      keywords=about['__keywords__'],
      author=about['__author__'],
      author_email=about['__author_email__'],
      url=about['__url__'],
      install_requires=requires,
      packages=find_packages(exclude=['pypandoc']),
      entry_points={
        "console_scripts": [
            'ecs-mon = ecs_mon.ecs_mon:main'
        ]
        },
      license=about['__license__'],
      classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        ]
     )