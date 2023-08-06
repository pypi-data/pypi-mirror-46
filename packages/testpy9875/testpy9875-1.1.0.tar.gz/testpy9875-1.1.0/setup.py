from distutils.core import setup
from distutils.extension import Extension

setup(
    name='testpy9875',
    author="zztech",
    author_email="zz1036@qq.com",
    description="一个测试包而已，玩玩而已。",
    long_description="就不要长描述了。啊",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    version="1.1.0",
    url="http://blog.yoqi.me",
    packages=['testpy'],
    zip_safe=True
)
