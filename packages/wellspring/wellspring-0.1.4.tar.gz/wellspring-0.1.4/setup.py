from setuptools import setup

setup(name='wellspring',
      version='0.1.4',
      description='Custom pyspark package to work with Databricks',
      url='https://pypi.org/project/wellspring/',
      author='Tarun Rana',
      author_email='tarun.rana@henkel.com',
      license='MIT',
      packages=['wellspring'],
      install_requires=['pyspark','DateTime','pytz','pandas','numpy','six','IPython'],
      zip_safe=False)