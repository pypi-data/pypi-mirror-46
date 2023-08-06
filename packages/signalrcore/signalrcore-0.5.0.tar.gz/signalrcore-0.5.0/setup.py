import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signalrcore",
    version="0.5.0",
    author="mandrewcito",
    author_email="anbaalo@gmail.com",
    description="A Python SignalR Core client ",
    keywords="signalrcore, client, invocation, auth, streamming, azure services ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mandrewcito/signalrcore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2"
    ],
)