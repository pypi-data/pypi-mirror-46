from setuptools import setup

__version__ = '19.5.0'
__credits__ = "Romain Thomas"
__license__ = "GNU GPL v3"
__maintainer__ = "Romain Thomas"
__email__ = "the.spartan.proj@gmail.com"
__status__ = "released"
__website__ = "https://github.com/astrom-tom/stpip"

setup(
   name = 'stpip',
   version = __version__,
   author = __credits__,
   packages = ['stpip'],
   entry_points = {'console_scripts': ['stpip = stpip.__main__:main',],},
   description = 'a pepy.tech webscraping for pypi download statistics',
   license = __license__,
   url = __website__,
   python_requires = '>=3.5',
   install_requires = [
       "requests >= 2.21.0",
       "bs4 >= 0.0.1"
   ],
   include_package_data=True,
)
