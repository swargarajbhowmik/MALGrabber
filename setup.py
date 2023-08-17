from setuptools import setup, find_packages

setup(
    name="malgrabber",
    version="1.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "asyncio",
        "aiohttp"
    ],
    author="Swargaraj Bhowmik",
    author_email="contact@swargarajbhowmik.me",
    license="MIT",
    url="https://github.com/swargarajbhowmik/malgrabber",
)
