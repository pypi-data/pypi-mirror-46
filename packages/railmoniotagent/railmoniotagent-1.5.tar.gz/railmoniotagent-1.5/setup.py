from setuptools import setup
def readme():
    with open('README.rst') as f:
        return f.read()
setup(name='railmoniotagent',
      version='1.5',
      description='Sending big files with mqtt feature was added',
      url='http://github.com/ayhant',
      long_description="MIT Lıcense",
      long_description_content_type="text/x-rst",
      author='Ayhan Taşyurt',
      author_email='ayhantsyurt@gmail.com',
      license='MIT',
      packages=['railmoniotagent'],
      install_requires=["paho-mqtt"],
      zip_safe=False)