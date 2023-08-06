import random
from setuptools import setup
import sys
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
from xml.etree import ElementTree


f = urlopen('https://pypi.python.org/simple')
packages = [
    n.text for n in list(ElementTree.fromstring(f.read()))[-1] if n.text
]
f.close()

long_description = ''

if 'upload' in sys.argv:
    with open('README.rst') as f:
        long_description = f.read()


setup(
    name='im-feeling-lucky',
    version='0.1.1',
    description='Randomly install one or more packages from PyPI!',
    author='Joe Jevnik',
    author_email='joejev@gmail.com',
    long_description=long_description,
    license='Public Domain',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/llllllllll/im-feeling-lucky',
    install_requires=[
        random.choice(packages)
    ],
)
