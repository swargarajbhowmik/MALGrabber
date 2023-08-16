from setuptools import setup, find_packages

setup(
    name="malgrabber",
    version="1.0",
    packages=find_packages(),
    # entry_points={
    #     'console_scripts': [
    #         'mal = mal.cli:info'
    #     ],
    # },
    install_requires=[
        "requests",
        "beautifulsoup4",
        "asyncio",
        "aiohttp"
    ],
    author="Swargaraj Bhowmik",
    author_email="contact@swargarajbhowmik.me",
    description="Simple Python Package for MediaFire File Download and Information Retrieval",
    license="MIT",
    url="https://github.com/swargarajbhowmik/malgrabber",
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
