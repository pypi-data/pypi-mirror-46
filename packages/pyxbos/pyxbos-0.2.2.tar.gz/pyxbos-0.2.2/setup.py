# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyxbos', 'pyxbos.drivers']

package_data = \
{'': ['*'],
 'pyxbos': ['wave/*', 'wavemq/*'],
 'pyxbos.drivers': ['dark_sky/api',
                    'dark_sky/api',
                    'dark_sky/api',
                    'dark_sky/config.yaml',
                    'dark_sky/config.yaml',
                    'dark_sky/config.yaml',
                    'dark_sky/dark_sky.py',
                    'dark_sky/dark_sky.py',
                    'dark_sky/dark_sky.py',
                    'hue/hue.py',
                    'hue/hue.py',
                    'hue/requirements.txt',
                    'hue/requirements.txt',
                    'parker/*',
                    'system_monitor/requirements.txt',
                    'system_monitor/requirements.txt',
                    'system_monitor/systemmonitor.py',
                    'system_monitor/systemmonitor.py',
                    'weather_current/*',
                    'weather_prediction/*']}

install_requires = \
['googleapis-common-protos>=1.5,<2.0',
 'grpcio-tools>=1.18,<2.0',
 'grpcio>=1.18,<2.0',
 'tlslite-ng>=0.7.5,<0.8.0']

setup_kwargs = {
    'name': 'pyxbos',
    'version': '0.2.2',
    'description': 'Python bindings for XBOS-flavored WAVEMQ and related services',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
