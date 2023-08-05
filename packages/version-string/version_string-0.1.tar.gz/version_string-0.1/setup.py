from setuptools import setup, find_packages

setup(name='version_string',
      version='0.1',
      url='https://github.com/Patibandha/version_string',
      license='MIT',
      author='Meet Patibandha',
      author_email='',
      description='compare two string',
      packages=find_packages(exclude=['tests']),
      # long_description=open('README.md').read(),
      zip_safe=False)