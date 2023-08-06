import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "minik-vk-bot-api-minik",
    version = "1.4.5",
    author = "MiniK1337",
    author_email = "minikkat1337@gmail.com",
    description = "Python VK BOT API",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/MiniK1337/py-bot-vk-api",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)