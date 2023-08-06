from setuptools import setup, find_packages

import codecs
import os


def read(fname):
    '''
    读取 README.md 作为长描述
    '''
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8").read()


setup(
    name='testpy9875',
    author="zztech",
    author_email="zz1036@qq.com",
    description="一个测试包而已，玩玩而已。",
    long_description=read("README.md"),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    version="1.2.0",
    url="http://blog.yoqi.me",
    packages=find_packages(),
)
