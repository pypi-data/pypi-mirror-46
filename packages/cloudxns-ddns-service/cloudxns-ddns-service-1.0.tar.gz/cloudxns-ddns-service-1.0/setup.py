#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='cloudxns-ddns-service',
                 version='1.0',
                 description='CloudXNS-API by with Djanggo web server',
                 author='qianfeng',
                 author_email='27805195@qq.com',
                 url=' https://www.cloudxns.net/',
                 long_description="Python restful api for CloudXNS.net",
                 long_description_content_type="text/markdown",
                 license="MIT",
                 platforms='python 3.6',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 install_requires=[
                     'certifi>=2019.3.9',
                     'chardet>=3.0.4',
                     'Django>=2.1.8,<2.2',
                     'djangorestframework>=3.9.4',
                     'httplib2>=0.12.3',
                     'idna>=2.8',
                     'pytz>=2019.1',
                     'requests>=2.22.0',
                     'urllib3>=1.25.3',
                 ]
                 )
