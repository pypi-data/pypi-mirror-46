import setuptools

setuptools.setup(
    name="monkeytype_sqlalchemy",
    description="A SQLAlchemy backed call trace store for MonkeyType",
    long_description_content_type='text/markdown',
    long_description=open("readme.md", "r").read(),
    author="Disruptive Labs",
    author_email="oss+monkeytype_sqlalchemy@comanage.com",
    version="0.1",
    packages=setuptools.find_packages(),
    install_requires=["monkeytype", "sqlalchemy"],
    license="BSD",
    url="https://github.com/DisruptiveLabs/MonkeyType_SQLAlchemy",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
