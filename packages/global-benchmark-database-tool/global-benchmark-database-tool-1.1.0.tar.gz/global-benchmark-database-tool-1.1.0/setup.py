import os
from os.path import join

from flask import json
from setuptools import setup

gbd_dir = '.gbd'
config_dir = 'conf'
config_file = 'conf.json'
db_dir = 'db'
db_file = 'local.db'

home = os.environ['HOME']
sys_dir = join(home, gbd_dir)
if not os.path.isdir(sys_dir):
    os.mkdir(sys_dir)
config_path = join(sys_dir, config_dir)
if not os.path.isdir(config_path):
    os.mkdir(config_path)
config = os.path.join(config_path, config_file)
open(config, 'w').close()
f = open(config, 'w')
f.write('{}\n'.format(json.dumps({'{}'.format(config_dir): '{}'.format(config)})))
f.close()
local_db_path = join(sys_dir, db_dir)
if not os.path.isdir(local_db_path):
    os.mkdir(local_db_path)
db = os.path.join(local_db_path, db_file)
f = open(db, 'w')
f.close()

setup(name='global-benchmark-database-tool',
      version='1.1.0',
      description='A tool for global benchmark management',
      long_description=open('README.md', 'rt').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/Weitspringer/gbd',
      author='Markus Iser, Luca Springer',
      author_email='',
      license='MIT',
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
      ],
      packages=['gbd_tool', 'gbd_tool/database',
                'gbd_tool/hashing'],
      include_package_data=True,
      install_requires=[
          'flask',
          'setuptools',
          'tatsu',
      ],
      zip_safe=False)
