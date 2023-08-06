from setuptools import setup, find_packages
import os
import sys
import re
import shutil


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def read_all(f):
    with open(f) as I:
        return I.read()

requirements = map(str.strip, open("requirements.txt").readlines())

version = get_version('yachain')

if sys.argv[-1] == 'publish':
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('yachain.egg-info')
    sys.exit()

setup(name='yachain',
      version=version,
      description="YAML parser",
      long_description=read_all("README.rst"),
      classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
      ],  # Get from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='YAML parser configuration',
      author='F. Brekeveld',
      author_email='f.brekeveld@gmail.com',
      url='http://github.com/hootnot/yachain',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
