#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This script is used to build and generate asvprotobuf files from
protocol buffers package
'''

import sys
import os
import asvprotobuf

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

if sys.version_info.major != 3:
    raise SystemError("Python version 2 is installed. Please use Python 3.")

if sys.platform not in ["linux2", "linux", "darwin"]:
    raise SystemError("This package cannot be installed on Windows or Cygwin.")

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
URL = "https://github.com/protocolbuffers/protobuf/releases/download/%s/protoc-%s-%s-x86_%d.zip"
OS_BIT = 32 if sys.maxsize < 2**32 else 64
OS_PLATFORM = "linux" if sys.platform in ["linux", "linux2"] else "osx"
VERSION = asvprotobuf.__version__

README = open(os.path.join(BASE_PATH, "README.md"), "r").read()
REQUIREMENTS = open(os.path.join(BASE_PATH, "requirements.txt")).read().split("\n")

def get_protobuf_version():
    '''This function returns the protobuf version'''
    for requirement in REQUIREMENTS:
        if "protobuf" in requirement:
            return requirement.split("=")[-1]
    return "3.6.1"
PROTOBUF_VERSION = get_protobuf_version()

URL = URL % (PROTOBUF_VERSION, PROTOBUF_VERSION, OS_PLATFORM, OS_BIT)

if not os.path.exists(os.path.join(BASE_PATH, "protoc.zip")):
    os.system("curl -L %s -o protoc.zip --silent" % (URL))
os.system("unzip -q protoc.zip")
if sys.platform == "darwin":
    os.system("./bin/protoc -I %s --python_out='%s' asvprotobuf/*.proto" % (BASE_PATH, BASE_PATH))
else:
    os.system("./bin/protoc --python_out='%s' asvprotobuf/*.proto" % (BASE_PATH))
os.system("rm -r bin/ include/ readme.txt")

setup(
    name="asvprotobuf",
    version=VERSION,
    description="ASV API for using protobuf for serialization and deserialization of objects",
    long_description=README,
    long_description_content_type='text/markdown',
    author="Akash Purandare",
    author_email="akash.purandare@srmasv.in",
    url="https://github.com/akashp1997/asv_protobuf",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license="BSD-3-Clause",
    test_suite="test",
    zip_safe=True,
    keywords="asvprotobuf",
)
