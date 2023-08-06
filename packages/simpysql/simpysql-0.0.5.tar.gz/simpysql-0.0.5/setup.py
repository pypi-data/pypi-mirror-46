import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpysql",
    version="0.0.5",
    author="jeanku",
    author_email="",
    description="A simple mysql orm base on pymysql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["simpysql"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pymysql',
        'pandas',
        'configparser',
        'DBUtils',
    ],
    entry_points={
        "console_scripts": ['simpysql = DBModel:DBModel']
    },
    keywords='MySQL ORM',
    python_requires='>=3',
)

'''
step1: python3 setup.py sdist bdist_wheel
step2: python3 -m twine upload dist/*
'''