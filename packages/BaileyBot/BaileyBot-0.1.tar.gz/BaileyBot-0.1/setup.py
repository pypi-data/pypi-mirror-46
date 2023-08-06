from setuptools import setup, find_packages
setup(
    name="BaileyBot",
    version="0.1",
    packages=find_packages(),
    scripts=['BaileyBot.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['yagmail>=0.11.200'],

    # metadata to display on PyPI
    author="Barry",
    author_email="lordbasilofcsu@gmail.com",
    description="This is an email bot.",
    license="PSF",
    keywords="BaileyBot email bot emailbot LordBasil SaintBasil",
    url="https://sites.google.com/view/python3-baileybot",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://sites.google.com/view/python3-baileybot",
        "Documentation": "https://sites.google.com/view/python3-baileybot",
        #"Source Code": "https://code.example.com/HelloWorld/",
    }

    # could also include long_description, download_url, classifiers, etc.
)
