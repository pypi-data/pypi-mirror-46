from pathlib import Path

from setuptools import setup, find_packages


readme = Path(__file__).parent.joinpath('README.md')
if readme.exists():
    with readme.open() as f:
        long_description = f.read()
else:
    long_description = '-'


setup(
    name='yoctol-argparse',
    version='0.1.0',
    description='Argument Parser create by Yoctol',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    packages=find_packages(),
    author='noobOriented',
    author_email='jsaon@yoctol.com',
    url='',
    license='MIT',
    install_requires=[],
)
