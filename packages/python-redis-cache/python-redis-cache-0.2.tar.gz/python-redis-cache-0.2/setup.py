from setuptools import setup, find_packages

setup(name='python-redis-cache',
      version='0.2',
      description='Basic Redis caching for functions',
      url='http://github.com/taylorhakes/python-redis-cache',
      author='Taylor Hakes',
      license='MIT',
      packages=find_packages(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'mock', 'fakeredis'],
)