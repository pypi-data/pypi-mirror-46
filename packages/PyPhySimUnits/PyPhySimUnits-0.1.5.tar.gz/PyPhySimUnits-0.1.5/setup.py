from distutils.core import setup
from glob import glob

packages = glob('PyPhySimUnits/*')
packages.append('PyPhySimUnits')
packages  = [p for p in packages if '__init__.py' not in p]

setup(
  name = 'PyPhySimUnits',
  packages = packages,
  version = '0.1.5',
  license='MIT',
  description = 'Repo for double-checking unit conversions and calculations',
  author = 'Christopher Auld',
  author_email = 'auld.chris.10@gmail.com',
  url = 'https://github.com/user/chupin10/PyPhySimUnits',
  download_url = 'https://github.com/chupin10/PyPhySimUnits/archive/0.1.5.tar.gz',
  keywords = ['Units', 'Engineering', 'Physics', 'Simulation'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
