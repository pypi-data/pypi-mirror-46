from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '1.0.0'

setup(name='purrito',
      version=version,
      author='Anett Balázsics',
      email='balazsicsanett@gmail.com',
      description="ETL tool for transfering data from MongoDB to PostgreSQL",
      url='https://boosterfuels.github.io/purr',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Database"
      ],
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              'purr = etl.__main__:main'
          ]
      }
      )
