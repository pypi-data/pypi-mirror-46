from setuptools import setup

requirements = [
    'aiohttp',
    'mixpanel'
]

setup(name='aiomixpanel',
      version='1.1.0',
      description='aiohttp-based mixpanel consumer for python3',
      url='https://github.com/jonathan-shemer/aiomixpanel',
      author='Jonathan Shemer',
      license='GNUv3',
      packages=['aiomixpanel'],
      install_requires=requirements
      )
