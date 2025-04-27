from setuptools import setup, find_packages

setup(
    name="timelapse_ig_reels",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "moviepy>=1.0.3,<2.0.0",
        "python-dotenv>=0.19.0",
        "instagrapi>=1.16.30",
        "pathlib>=1.0.1"
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-mock>=3.10.0',
            'pytest-cov>=4.0.0',
        ],
    },
    package_data={
        'timelapse_ig_reels': ['resources/*.json'],
    },
    include_package_data=True,
    python_requires=">=3.8",
    author="Tim Barker",
    author_email="timo.barker@gmail.com",
    description="Create and upload timelapse videos to Instagram Reels with music",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/timo-barker/timelapse_ig_reels",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)