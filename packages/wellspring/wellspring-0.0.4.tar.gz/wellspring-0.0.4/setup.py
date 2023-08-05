from setuptools import setup

setup(name='wellspring',
      version='0.0.4',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Tarun Rana',
      author_email='tarun.rana@henkel.com',
      license='private',
      packages=['wellspring'],
      install_requires=[
          'pyspark','datetime',
      ],
      zip_safe=False)