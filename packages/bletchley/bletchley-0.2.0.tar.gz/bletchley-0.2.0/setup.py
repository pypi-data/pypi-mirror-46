import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bletchley",
    version="0.2.0",
    author="manny",
    author_email="manny@cyber-wizard.com",
    description="A collection of historical ciphers and cryptanalysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/manny_cyber_wizard/bletchley",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.16.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Development Status :: 3 - Alpha",
    ],
    project_urls={ 
        'Bug Reports': 'https://gitlab.com/manny_cyber_wizard/bletchley/issues',
        'Say Thanks!': 'https://saythanks.io/to/MannyCyber',
        'Source': 'https://gitlab.com/manny_cyber_wizard/bletchley',
    },
)