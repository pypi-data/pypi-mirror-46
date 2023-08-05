import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KnapKingsTest2",
    version="0.0.1",
    author="Greg Dray and Dylan Mortimer",
    author_email="dmortimer@middlebury.edu",
    description="Daily Fantasy Sports Optimization Package",
    long_description="Daily Fantasy Sports Optimization Package",
    long_description_content_type="text/markdown",
    py_modules=['Knapsack','runKnap','Player'],
    package_dir={'': 'KnapKings'},
    url="https://github.com/dylanmortimer12/KnapKings",
    install_requires=[
          'numpy',
          'beautifulsoup4',
          'requests',
          'csv',
          're',
          'urllib',
          'datetime',
          'random'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)