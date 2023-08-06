# create distribution and upload to pypi.org with:
#   $ python setup.py sdist bdist_wheel
#   $ twine upload dist/*

from setuptools import setup, find_packages

setup(name='arctic_cod_detector',
      version='0.0.4',
      description="Neural-network detector of grunts made by arctic cod",
      url='https://gitlab.meridian.cs.dal.ca/data_analytics_dal/projects/arctic_cod_detector',
      author='Oliver Kirsebom, Fabio Frazao',
      author_email='oliver.kirsebom@dal.ca, fsfrazao@dal.ca',
      license='GNU General Public License v3.0',
      packages=find_packages(),
      install_requires=[
          'ketos==1.0.2',
          ],
      entry_points = {"console_scripts": ["arctic-cod-detector=bin.run:main"]},
      data_files=[('config/arctic-cod-detector', ['cnn/checkpoint','cnn/cnn.data-00000-of-00001','cnn/cnn.index','cnn/cnn.meta'])],
      include_package_data=True,
      zip_safe=False)
