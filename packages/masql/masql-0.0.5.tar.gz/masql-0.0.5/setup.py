#!/usr/bin/env python

from distutils.core import setup

setup(name='masql',
      version='0.0.5',
      description='mysql for humans',
      long_description=open('README.md', 'r').read(),
      long_description_content_type="text/markdown",
      author='Ma HaoYang',
      author_email='martinlord@foxmail.com',
      url='https://github.com/mahaoyang/masql/tree/master',
      packages=['mysql'],
      license='LICENSE.txt',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries'
      ],
      )

# python setup.py sdist && python setup.py sdist upload && pip install --upgrade masql
# https://www.jianshu.com/p/0dbb6f0c3b11
# http://www.mahaoyang.cn/post/12/
