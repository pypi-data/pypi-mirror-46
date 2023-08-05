from setuptools import setup, find_packages

setup(
    name="hrisapi",
    version="0.0.1",
    packages=["hrisapi"],
    url="https://github.com/deep-compute/hrisapi",
    install_requires=[
        "basescript==0.2.8",
        "graphene==2.1.3"
    ],
    author="deep-compute",
    author_email="contact@deepcompute.com",
    description="Human Resource Information Systems API",
    keywords=["hris", "hrisapi", "hrms"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "hrisapi = hrisapi:main",
        ]
    }
)
