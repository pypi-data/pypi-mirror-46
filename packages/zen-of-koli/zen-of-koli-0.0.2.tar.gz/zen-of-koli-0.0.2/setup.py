
from setuptools import setup, find_packages

setup(
    name='zen-of-koli',
    version='0.0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Ultimite guide to life, python and all.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maroshmka/zen-of-koli',
    author='Mario Hunka',
    author_email='hunka.mario@gmail.com'
)