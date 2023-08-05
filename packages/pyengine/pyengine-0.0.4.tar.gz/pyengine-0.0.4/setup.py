#encoding=utf-8
from setuptools import setup, find_packages
with open('./pyengine/ReadMe.md','r',encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name = "pyengine",
    version = "0.0.4",
    keywords = ["py", "engine","run"],
    description = '''
    一个运行Python代码的web接口
    A web interfacerun who can run Python code 
    ''',
    long_description = long_desc,
    license = "Apache License V2.0",

    url = "http://www.gitee.com",
    author = "liuyancong",
    author_email = "1437255447@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['Flask==1.0.2','Flask-Script==2.0.6'],

    scripts = [],
    entry_points = {
        'console_scripts': [
            'pyengine = pyengine.app:main'
        ]
    }
)
