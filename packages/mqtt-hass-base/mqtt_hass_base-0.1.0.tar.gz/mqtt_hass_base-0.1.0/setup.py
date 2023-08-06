
import sys

from setuptools import setup
from mqtt_hass_base import VERSION

if sys.version_info < (3,7):
    sys.exit('Sorry, Python < 3.7 is not supported')

install_requires = list(val.strip() for val in open('requirements.txt'))
tests_require = list(val.strip() for val in open('test_requirements.txt'))

setup(name='mqtt_hass_base',
      version=VERSION,
      description='Bases to build mqtt daemon compatible with Home Assistant',
      author='Thibault Cohen',
      author_email='titilambert@gmail.com',
      url='http://gitlab.com/titilambert/mqtt_hass_base',
      package_data={'': ['LICENSE.txt']},
      include_package_data=True,
      packages=['mqtt_hass_base'],
      license='Apache 2.0',
      install_requires=install_requires,
      tests_require=tests_require,
      classifiers=[
        'Programming Language :: Python :: 3.7',
      ]

)
