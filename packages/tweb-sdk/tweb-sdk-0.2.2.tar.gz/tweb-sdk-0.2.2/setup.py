#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

ver = '0.2.2'

setup(
    name='tweb-sdk',
    version=ver,
    description=(
        'Web server framework based on tornado'
    ),
    long_description='Docs for this project are maintained at https://gitee.com/qcc100/tweb-sdk.git.',
    author='Yang Chunbo',
    author_email='ycb@microto.com',
    maintainer='Yang Chunbo',
    maintainer_email='ycb@microto.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/qcc100/tweb-sdk.git',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'aliyun-python-sdk-core==2.11.4',
        'aliyun-python-sdk-core-v3==2.11.4',
        'aliyun-python-sdk-kms==2.5.0',
        'APScheduler==3.5.3',
        'asn1crypto==0.24.0',
        'bitarray==0.8.3',
        'certifi==2018.10.15',
        'cffi==1.11.5',
        'chardet==3.0.4',
        'crcmod==1.7',
        'cryptography==2.3.1',
        'DBUtils==1.3',
        'idna==2.7',
        'kafka-python==1.4.4',
        'oss2==2.6.0',
        'pycparser==2.19',
        'pycryptodome==3.7.2',
        'pymongo==3.7.2',
        'PyMySQL==0.9.2',
        'pytz==2018.7',
        'redis==2.10.6',
        'requests==2.20.1',
        'six==1.11.0',
        'tornado==5.1.1',
        'tzlocal==1.5.1',
        'urllib3==1.24.1',
        'websocket-client==0.54.0'
    ]
)
