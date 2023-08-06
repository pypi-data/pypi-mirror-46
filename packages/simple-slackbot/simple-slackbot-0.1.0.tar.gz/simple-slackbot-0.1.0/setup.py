import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='simple-slackbot',
    version='0.1.0',
    scripts=[],
    author="Chris George",
    author_email="chrisg1622@gmail.com",
    description="A simple python wrapper for the slack API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisg1622/slackbot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ]
)
