from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='easytoolset',
      version='0.7',
      description='The easy tools in the world',
      long_description=readme(),
      url='http://github.com/maxis1314',
      author='Daniel',
      author_email='maxis1314@163.com',
      scripts=['bin/easytoolset-joke'],
      license='MIT',
      packages=['easytoolset'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)
