from setuptools import setup
import sys


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)


if CURRENT_PYTHON <= REQUIRED_PYTHON:
    raise SystemExit("Use Python 3 (or higher) only")

def readme():
    with open('README.rst', 'r') as w:
        return w.read()


setup(name='filestat',
      version='0.2.3',
      classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: End Users/Desktop',
                'Intended Audience :: Developers',
                'Intended Audience :: Education',
                'Intended Audience :: System Administrators',
                'Operating System :: MacOS :: MacOS X',
                'Operating System :: POSIX',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3 :: Only',
                'Topic :: Office/Business',
                'Topic :: Software Development :: Bug Tracking',
                ],
      description='A command line library for file monitoring.',
      long_description=readme(),
      url='https://github.com/zxalif/filestat/',
      author='Alif Jahan',
      keywords='filestat stats file monitoring details',
      author_email='sajeeb162537@gmail.com',
      license='MIT',
      packages=['filestat'],
      include_package_data=True,
      zip_safe=False)
