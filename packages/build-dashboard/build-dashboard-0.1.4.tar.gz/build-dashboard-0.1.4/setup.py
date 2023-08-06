from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as long_d_f:
    long_description = long_d_f.read()

setup(
  name = 'build-dashboard',
  packages = ['build_dashboard'],
  version = '0.1.4',
  description = 'Buildbot CLI Dashboard',
  long_description = long_description,
  long_description_content_type = 'text/x-rst',
  author = 'Jeffrey Hill',
  author_email = 'jeff@reverentengineer.com',
  url = 'https://github.com/ReverentEngineer/build-dashboard',
  keywords = ['buildbot', 'continuous integration', 'ci', 'cli' ],
  classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 3',
      ],
  entry_points={
      'console_scripts': [
            'build-dashboard = build_dashboard.cli:main'
        ]
    },
  install_requires = ['aiohttp', 'toml', 'asciimatics','cachetools'],
)
