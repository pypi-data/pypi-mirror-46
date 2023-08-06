#!/usr/bin/env python

__author__ = "Pawel Kowalik"
__copyright__ = "Copyright 2018, 1&1 IONOS SE"
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Pawel Kowalik"
__email__ = "pawel-kow@users.noreply.github.com"
__status__ = "Beta"

from setuptools import setup

setup(name='id4me-rp-client',
      version='0.0.20',
      description='Python client library for ID4me protocol - Relying Party side. See: https://id4me.org',
      long_description_content_type="text/markdown",
      long_description=open('README.md').read(),
      author='Pawel Kowalik',
      author_email='pawel-kow@users.noreply.github.com',
      url='https://gitlab.com/ID4me/id4me-rp-client-python',
      license='https://gitlab.com/ID4me/id4me-rp-client-python/blob/master/LICENSE',
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
      ],
      packages=[
          'id4me_rp_client',
      ],
      install_requires=[
          'dnspython >= 1.15.0',
          'six >= 1.11.0',
          'future >= 0.16.0',
          'jwcrypto >= 0.5.0',
      ],
      tests_require=[
          'unittest2 >= 1.1.0',
          'typing >= 3.5.3.0',
      ]
)
