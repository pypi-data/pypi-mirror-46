"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wikiwho_pickle",
    version="1.1.1",
    # Author details
    author="",
    author_email="wikiwho@gesis.org",
    description="Open the internal structure of a WikiWho pickle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gesiscss/wikiwho_pickle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # What does your project relate to?
    keywords='wikipedia wikiwho revisions content authorship',
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['WikiWho==1.0.3', 'python-dateutil>=2.7.3']
)
