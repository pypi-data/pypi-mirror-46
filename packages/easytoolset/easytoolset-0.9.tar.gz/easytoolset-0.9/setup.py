from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='easytoolset',
      version='0.9',
      description='The easy tools in the world',
      long_description=readme(),
      url='http://github.com/maxis1314',
      author='Daniel',
      author_email='maxis1314@163.com',
      #scripts=['bin/funniest-joke'],
      entry_points = {
        'console_scripts': ['joke=easytoolset.command_line:main'],
      },
      license='MIT',
      packages=['easytoolset'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)
