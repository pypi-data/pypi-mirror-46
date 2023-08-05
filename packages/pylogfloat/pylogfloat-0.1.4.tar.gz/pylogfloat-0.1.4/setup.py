from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pylogfloat',
      version='0.1.4',
      description='A numeric type for Python storing floats in log space for increased precision, allowing positive and negative float computations (arithmetic and logical operations)',
      long_description=readme(),
      url='https://bsennblad@bitbucket.org/bsennblad/pylogfloat.git',
      author='Bengt Sennblad',
      author_email='bengt.sennblad@scilifelab.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy',
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
      )
