dtool CLI commands for configuring dtool settings
=================================================

.. image:: https://badge.fury.io/py/dtool-config.svg
   :target: http://badge.fury.io/py/dtool-config
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtool-config.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtool-config
   :alt: Travis CI build status (Linux)

.. image:: https://codecov.io/github/jic-dtool/dtool-config/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtool-config?branch=master
   :alt: Code Coverage


Installation
------------

Installation using ``pip``::

    pip install dtool-config

Example usage
-------------

Setting the user name and email::

    dtool config user name "Marie Curie"
    dtool config user email marie.curie@sorbonne-universite.fr

Setting the download cache::

    mkdir /tmp/dtool
    dtool config cache /tmp/dtool


Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-info <https://github.com/jic-dtool/dtool-create>`_
- `dtool-create <https://github.com/jic-dtool/dtool-create>`_
