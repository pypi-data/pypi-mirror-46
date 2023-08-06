from setuptools import setup

setup(name='easy_readme',
      version='0.2.0',
      description='Generate a barebones readme based off of your directory',
      url='http://github.com/mcabrams/easy_readme',
      author='Matthew Carlos Abrams',
      license='MIT',
      packages=['easy_readme'],
      zip_safe=False,
      install_requires=['PyInquirer>=1,<2'],
      entry_points={
          'console_scripts': ['easy-readme=easy_readme.command_line:main'],
      })
