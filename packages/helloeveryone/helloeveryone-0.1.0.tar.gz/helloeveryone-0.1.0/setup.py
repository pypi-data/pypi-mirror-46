
from os import path
from distutils.core import setup

setup(
    name="helloeveryone",
    packages=["helloeveryone"],
    version="0.1.0",
    license="MIT",
    description="Translate Hello Everyone in random languages with Google Translate API",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="John Naylor",
    author_email="ramdev@vcu.edu",
    url="https://github.com/vcuramdev/HelloEveryone",
    download_url="https://github.com/vcuramdev/HelloEveryone/archive/v_1.0.tar.gz",
    keywords=["translate", "google"],
    entry_points={"console_scripts": ["hello=helloeveryone.translate:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
