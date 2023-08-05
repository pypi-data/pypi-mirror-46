import setuptools
from datetime import datetime
import re
import os

with open("README.md","r") as fh:
  long_description = fh.read()

with open('hushpush/constant.py') as f:
  constants = f.read()

version = re.search(r'^\s*VERSION\s*=\s*[\'"](.+)[\'"]\s*$', constants, re.MULTILINE).group(1)
prod_release = os.getenv("HUSH_PROD_VERSION", False)

def get_version_suffix_string(prod_release):
  dt = datetime.today().strftime('%Y%m%d%H%M')
  if prod_release:
    return ""
  else:
    return ".dev" + dt

setuptools.setup(
  name="hush-push",
  version=version + get_version_suffix_string(prod_release),
  author="hawry",
  entry_points = {
    "console_scripts": ["hushpush=hushpush.hushpush:main"]
  },
  author_email="hawry@hawry.net",
  description="Push your git-secret protected configuration parameters to AWS Parameter Store using roles for multiple accounts",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/hawry/hush-push",
  packages=setuptools.find_packages(),
  install_requires=[
    "argparse",
    "coloredlogs",
    "boto3",
    "terminaltables",
    "gitpython",
  ],
  classifiers=[
    "Programming Language :: Python :: 3.5",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Development Status :: 3 - Alpha"
  ]
)
