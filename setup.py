from setuptools import setup, find_packages

setup(
    name="xparrot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=8.3.0",
        "python-dotenv>=0.19.0",
        "SQLAlchemy>=2.0.25",
    ],
)
