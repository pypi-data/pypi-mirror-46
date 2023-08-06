import os
from io import open
import hashlib
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "click",
    "qrcode",
    "pillow",
]


setup(
    name="qrimg",
    version="0.1.0",
    description="Generate QRCode Image",
    long_description=long_description,
    url="https://github.com/appstore-zencore/qrimg",
    author="zencore",
    author_email="appstore@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['qrimg'],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=['qrimg'],
    entry_points={
        'console_scripts': "qrimg = qrimg:main"
    },
)