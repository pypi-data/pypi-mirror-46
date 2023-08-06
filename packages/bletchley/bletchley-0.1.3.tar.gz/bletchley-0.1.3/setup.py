import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bletchley",
    version="0.1.3",
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
)