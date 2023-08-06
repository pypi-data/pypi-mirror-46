from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="moderage-python",
    version="0.1.6",
    author="Chris Bamford",
    author_email="chrisbam4d@gmail.com",
    description="Mode Rage python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/chrisbam4d/moderage-python-client",
    packages=find_packages(),
    install_requires=[
        'requests==2.21.0',
        'python-magic==0.4.15',
        'requests-toolbelt==0.9.1',
        'tqdm==4.31.1',
        'tinydb==3.13.0',
        'PyYAML==5.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)