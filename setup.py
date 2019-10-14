from setuptools import find_packages, setup

setup(name='Choose activity',
      version='1.0',
      description='Choose a random activity to do from a list',
      author='Jacopo Farina',
      packages=find_packages(),
      # dependency only for tests, yet to investigate the best practice
      # install_requires=[''],
      )
