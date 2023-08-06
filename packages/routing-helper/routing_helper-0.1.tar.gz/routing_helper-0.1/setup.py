from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='routing_helper',
      version='0.1',
      description='Helper functions for sail_route.jl',
      long_description=readme(),
      url='https://github.com/TAJD/route_helpers',
      author='Thomas Dickson',
      author_email='thomas.dickson@soton.ac.uk',
      license='MIT',
      packages=['routing_helper'],
      install_requires=['xarray',
                        'xesmf',
                        'shapely'],
      zip_safe=False)
