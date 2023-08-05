from setuptools import setup
from styled import STYLED_VERSION

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name='styled',
    version=STYLED_VERSION,
    packages=['styled'],
    url='',
    license='Apache 2.0',
    author='Paul K. Korir, PhD',
    author_email='pkorir@ebi.ac.uk, paul.korir@gmail.com',
    description='Style your terminal with ease!',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
