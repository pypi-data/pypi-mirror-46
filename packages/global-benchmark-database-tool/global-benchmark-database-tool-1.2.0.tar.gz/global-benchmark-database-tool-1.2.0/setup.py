from setuptools import setup

setup(name='global-benchmark-database-tool',
      version='1.2.0',
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
      entry_points={
          'console_scripts': [
              'global-benchmark-database-tool = gbd_tool.__init__:main'
          ]
      },
      zip_safe=False)
