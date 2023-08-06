from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mysqlwrapperpackage1',
      version='v1.2',
      description='MySQL Python Wrapper Package',
      long_description=long_description,
      author='Sharon Waithira',
      author_email='sharonwaithii@gmail.com',
      url='https://github.com/Sharonsyra',
      download_url='https://github.com/Sharonsyra/MySQLWrapperPackage/archive/v1.2.tar.gz',
      license='MIT',
      install_requires=[
          'pymsql',
          'injector',
      ],
      packages=['MySQLWrapperPackage'],
      zip_safe=False)
