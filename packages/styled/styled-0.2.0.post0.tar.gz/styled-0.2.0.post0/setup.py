from setuptools import setup

from styled import STYLED_VERSION

with open(u"README.md") as fh:
    long_description = fh.read()

setup(
    name=u'styled',
    version=STYLED_VERSION,
    packages=[u'styled'],
    url='',
    license=u'Apache 2.0',
    author=u'Paul K. Korir, PhD',
    author_email=u'pkorir@ebi.ac.uk, paul.korir@gmail.com',
    description=u'Style your terminal with ease!',
    long_description=long_description,
    long_description_content_type=u'text/markdown',
    classifiers=[
        u"Development Status :: 4 - Beta",
        u"Environment :: Console",
        u"Intended Audience :: Developers",
        u"License :: OSI Approved :: Apache Software License",
        u"Operating System :: OS Independent",
        u"Programming Language :: Python :: 2",
        u"Programming Language :: Python :: 2.7",
        u"Programming Language :: Python :: 3",
        u"Programming Language :: Python :: 3.4",
        u"Programming Language :: Python :: 3.5",
        u"Programming Language :: Python :: 3.6",
        u"Programming Language :: Python :: 3.7",
        u"Topic :: Software Development :: Libraries :: Python Modules",
        u"Topic :: Terminals",
        u"Topic :: Text Processing",
        u"Topic :: Text Processing :: Markup",
        u"Topic :: Utilities",
    ]
)
