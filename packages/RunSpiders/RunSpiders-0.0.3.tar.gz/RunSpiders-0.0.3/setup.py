# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="RunSpiders",
    version="0.0.3",
    description="Some predefined web crawlers",
    long_description=open('README.rst').read(),
    author='Ijustwantyouhappy',
    author_email='18817363043@163.com',
    maintainer='',
    maintainer_email='',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    package_data = {
        '': ['*.recipe']
    },
    platforms=["all"],
    url='',
    install_requires=["requests>=2.14.2",
                      "beautifulsoup4>=4.5.1",
                      "jinja2>=2.10.1"],
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
        'Programming Language :: Python :: 3.7'
    ]
)