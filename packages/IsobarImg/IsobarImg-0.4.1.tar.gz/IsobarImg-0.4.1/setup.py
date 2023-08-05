from setuptools import setup
import re

with open('IsobarImg/__init__.py') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with open('README.rst') as f:
    readme = f.read()

setup(name='IsobarImg',
      version=version,
      description='isobar python image library',
      long_description=readme,
      url='https://github.com/wwwins/IsobarImgPy',
      author='wwwins',
      author_email='cphuang72@gmail.com',
      license='MIT',
      packages=['IsobarImg'],
      zip_safe=False,
      keywords='IsobarImg',
      install_requires=[
          'Pillow',
          'opencv-contrib-python'
      ])
