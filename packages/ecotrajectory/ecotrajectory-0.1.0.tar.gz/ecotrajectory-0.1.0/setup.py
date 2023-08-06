from distutils.core import setup
setup(
  name = 'ecotrajectory',
  packages = ['ecotrajectory'],
  version = '0.1.0',
  #include_package_data=True,
  #package_data= {'geneflow': ['data/*']},
  license='GNU General Public License v3 (GPLv3)',
  description = 'A package for simulating simple ecological communities.',
  author = 'Sky Jones',
  author_email = 'rsajones94@gmail.com',
  url = 'https://github.com/rsjones94',
  download_url = 'https://github.com/rsjones94/ecotrajectory/archive/v0.1.0.tar.gz',
  keywords = [
              'ecology', 'evolution', 'drift', 'genetic', 'algorithm',
              'simulation'
              ],
  install_requires=[
          'numpy',
          'matplotlib'
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)
