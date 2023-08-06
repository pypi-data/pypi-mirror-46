from setuptools import setup
setup(name='mlagent',
      author='MLaaS',
      packages=['mlagent','mlagent/pyll'],
      include_package_data=True,
      install_requires=[
          'requests',
          'future',
          'numpy',
          'jsonpickle',
          'matplotlib',
          'networkx'
      ],
      entry_points = {
        'console_scripts': [
            'mlagent = mlagent.__main__:main',
        ]
      },
      version='10.2.0')
