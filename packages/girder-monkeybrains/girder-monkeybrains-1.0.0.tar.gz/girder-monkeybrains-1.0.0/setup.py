from setuptools import setup
setup(
    name='girder-monkeybrains',
    version='1.0.0',
    description='Displays monkey neurodevelopmental data.',
    url='https://github.com/girder/monkeybrains',
    maintainer='Kitware, Inc.',
    maintainer_email='kitware@kitware.com',
    packages=['girder_monkeybrains'],
    install_requires=['girder'],
    entry_points={
      'girder.plugin': [
          'monkeybrains = girder_monkeybrains:MonkeybrainsPlugin'
      ]
    }
)
