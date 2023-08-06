from distutils.core import setup
setup(
  name = 'PyPhySimUnits',
  packages = ['PyPhySimUnits'],
  version = '0.1.3',
  license='MIT',
  description = 'Repo for double-checking unit conversions and calculations',
  author = 'Christopher Auld',
  author_email = 'auld.chris.10@gmail.com',
  url = 'https://github.com/user/chupin10/PyPhySimUnits',
  download_url = 'https://github.com/chupin10/PyPhySimUnits/archive/0.1.3.tar.gz',
  keywords = ['Units', 'Engineering', 'Physics', 'Simulation'],
  install_requires=[
          'numpy',
          'typing',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
