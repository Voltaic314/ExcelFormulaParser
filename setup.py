from setuptools import setup, find_packages

setup(
    name="Excel-Helper-Framework",
    version="1.0.0",
    packages=find_packages(where="src"),  # Tells setuptools to package any Python packages found in src
    package_dir={"": "src"},  # Tells setuptools that the packages are under src directory
    author="Voltaic314",
    author_email="logan@stax.ai",
    description="A framework to break down Excel Formula strings into a parsable and modifiable JSON data structure.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'openpyxl',  # List your dependencies here
        # other dependencies...
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
