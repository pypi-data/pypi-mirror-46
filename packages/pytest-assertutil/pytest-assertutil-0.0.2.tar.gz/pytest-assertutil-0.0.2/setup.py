from setuptools import find_packages, setup
from pytest_assertutil import __version__

setup(name='pytest-assertutil',
      version=__version__,
      description='pytest-assertutil',
      long_description='',
      url='https://github.com/xyloon/pytest-assertutil',
      author='xyloon',
      author_email='xyloon@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
