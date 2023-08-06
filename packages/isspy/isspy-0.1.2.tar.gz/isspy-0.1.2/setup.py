from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='isspy',
      version='0.1.2',
      description='Get the international space station passes over your head',
      url='http://github.com/hydrius/isspy',
      author='A Fordham',
      author_email='A.fordham@iinet.net.au',
      license='MIT',
      packages=['isspy'],
      zip_safe=False)

