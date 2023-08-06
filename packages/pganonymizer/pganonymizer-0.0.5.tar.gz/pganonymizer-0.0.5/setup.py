import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pganonymizer",
    version="0.0.5",
    author="Pattarawut Imamnuaysup",
    author_email="pattarawut@hot-now.com",
    description="Database anonymizer package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={'console_scripts': [
        'pganonymizer = pganonymizer.anonymize:main',
    ]},
    python_requires='>=3.5',
    install_requires=[
        'asyncpg', 'csj-parser', 'click', 'asyncio', 'pytest-asyncio'
    ],
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)