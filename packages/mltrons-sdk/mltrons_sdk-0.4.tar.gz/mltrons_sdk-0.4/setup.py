from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mltrons_sdk',
    version='0.4',
    description='Automated machine learning platform',
    long_description=readme,
    author='Muzammil Sharif',
    author_email='muzammil.sharif786@gmail.com',
    url='https://github.com/muz786/mltrons_sdk',
    license=license,
    packages=find_packages(),
    install_requires=[
       'requests',
    ]
)