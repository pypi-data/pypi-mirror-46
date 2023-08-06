from setuptools import setup

setup(
    name = 'manuf-ng',
    packages = ['manuf'],
    version = '1.0.0',
    description = 'Parser library for Wireshark\'s OUI database',
    author = 'Michael Huang and Daniel Leicht',
    url = 'https://github.com/daniel-leicht/manuf/',
    license = 'Apache License 2.0 or GPLv3',
    keywords = ['manuf', 'manuf-ng', 'mac address', 'networking'],
    entry_points = {
        'console_scripts': [
            'manuf=manuf.manuf:main'
        ],
    },
    package_data = {
        'manuf': ['manuf']
    },
)

