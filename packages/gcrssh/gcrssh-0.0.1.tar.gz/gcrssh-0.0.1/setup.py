from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='gcrssh',
    version="0.0.1",
    description='ssh to gcr',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='wy',
    url='',
    author_email='',
    license='MIT', 
    packages=find_packages(),
    scripts = ['gcrssh/main.py'],
    entry_points={
        'console_scripts': 'gcrssh = gcrssh.main:ssh'
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ]
)
