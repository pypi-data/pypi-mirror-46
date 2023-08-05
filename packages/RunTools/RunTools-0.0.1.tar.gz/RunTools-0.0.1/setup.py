# -*- coding: utf-8 -*-
# @Time     : 2019/5/13 10:15
# @Author   : Run 
# @File     : setup.py
# @Software : PyCharm

from setuptools import setup, find_packages

setup(
    name="RunTools",
    version="0.0.1",
    description="A Python library for transforming data format",
    long_description=open('README.rst').read(),
    author='Ijustwantyouhappy',
    author_email='18817363043@163.com',
    maintainer='nobody',
    maintainer_email='',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    # package_data = {
    #     '': ['*.hdf5', '*.html', '*.ipynb', '*.jpg', '*.npz']
    # },
    platforms=["all"],
    url='',
    install_requires=["numpy>=1.16.3",
                      "pandas>=0.23.4"],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)