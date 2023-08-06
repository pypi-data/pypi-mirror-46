from setuptools import setup

setup(name='gitgang',
      version='0.0.1',
      description='Reject pull-requests that are not from members of your gang.',
      url='https://github.com/brockfanning/gitgang',
      author='Brock Fanning',
      author_email='brockfanning@gmail.com',
      license='MIT',
      install_requires=[
          'requests',
          'pyyaml'
      ])