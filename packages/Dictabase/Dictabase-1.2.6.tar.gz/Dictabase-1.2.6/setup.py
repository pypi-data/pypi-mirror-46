from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['dictabase']
print('packages=', packages)

setup(
    name="Dictabase",

    version="1.2.6",
    # 1.2.6 added relational mapping
    # 1.2.5 changed README to rst
    # 1.2.4 updated README
    # 1.2.3 added dependencies
    # 1.2.2 changed from module to package
    # 1.2.1 updated readme
    # 1.1 updated readme

    packages=packages,
    install_requires=['dataset'],
    # scripts=['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires=['docutils>=0.3'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A database interface that mimics a python dictionary.",
    long_description=long_description,
    license="PSF",
    keywords="dictionary database dictabase grant miller sqlalchemy flask sqlite",
    url="https://github.com/GrantGMiller/dictabase",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/dictabase",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# python setup.py sdist bdist_wheel
# twine upload dist/*