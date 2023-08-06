import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantrautil",
    version="0.0.1",
    author="Quantra",
    author_email="ishan.s@quantinsti.com",
    description="To fetch the data from web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QuantInsti/Quantra-Courses/",
    packages=setuptools.find_packages(),
    install_requires=[            
          'fix_yahoo_finance>=0.1.0',
          'nsepy>=0.7',
          'iexfinance>=0.4.1'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',        
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)