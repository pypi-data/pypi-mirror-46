from setuptools import setup, find_packages

setup(name='flaskapptestjw',
      version='0.12',
      description='Test Flask app upload with pypi',
      long_description=open('README.md').read(),
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['Flask']
)