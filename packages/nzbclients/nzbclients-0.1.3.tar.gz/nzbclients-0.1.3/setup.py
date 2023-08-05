from setuptools import setup, find_packages

requires = [
    'requests>=2.19.0',
    'marshmallow>=3.0.0rc6'
]

setup(
    name="nzbclients",
    packages=find_packages(exclude=["tests*"]),
    version="0.1.3",
    license="MIT",
    description="A library of unofficial library of clients for interacting with programs that download NZB files.",
    author="Jeff Blakeney",
    author_email="jblakeneypypi@gmail.com",
    url="https://github.com/jblakeney/nzbclients",
    keywords=["radarr", "sabnzbd", "sonarr", "nzbdrone", "nzb"],
    install_requires=requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
