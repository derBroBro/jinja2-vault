import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jinja2-vault",
    version="0.0.2",
    author="Malte Brodersen",
    author_email="malte.brodersen@exoit.de",
    description="Extentsion to load vault screts in jinja templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/derBroBro/jinja2-vault",
    packages=setuptools.find_packages(),
    install_requires=[
        'hvac',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
