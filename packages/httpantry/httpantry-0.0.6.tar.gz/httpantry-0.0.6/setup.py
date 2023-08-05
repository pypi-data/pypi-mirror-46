import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httpantry",
    version="0.0.6",
    author="Rowen Felt, Zebediah Millslagle",
    author_email="rowenfelt@gmail.com, zmillslagle@gmail.com",
    description="Caches HTTP requests for faster, more efficient development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RowenFelt/httpantry",
    packages=['httpantry'],
    install_requires=[
          'pathlib',
          'requests',
          'flask',
          'configparser'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts" : [
            "httpantry = httpantry.command_line:main",
        ]
    }
)
