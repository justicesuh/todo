from setuptools import setup, find_packages

setup(
    name='todo',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'todo=todo:main',
        ]
    }
)
