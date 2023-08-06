from distutils.core import setup
import setuptools

setup(
  name='stackd',
  version='0.2',
  description='STACKD - A docker swarm deploy helper according to environment',
  url='https://gitlab.com/youtopia.earth/bin/stackd',
  download_url='https://gitlab.com/youtopia.earth/bin/stackd/-/archive/master/stackd-master.tar.gz',
  # download_url='https://gitlab.com/youtopia.earth/bin/stackd/-/archive/29f4ae605e472b497f2d77edb778edb9590fb2a2/stackd-29f4ae605e472b497f2d77edb778edb9590fb2a2.tar.gz',
  keywords = ['docker', 'docker-stack', 'env'],
  author='Idetoile',
  author_email='idetoile@protonmail.com',
  license='MIT',
  packages=setuptools.find_packages(),
  scripts=['stackd/__main__'],
  entry_points={
    'console_scripts': [
      'stackd = package.module:__main__'
    ]
  },
  install_requires=[
    'PyYAML',
    'deepmerge',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)