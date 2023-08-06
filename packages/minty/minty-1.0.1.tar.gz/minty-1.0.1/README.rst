.. _readme:

Description
============

This "Command and Query" module allows a developer to generate an abstraction around
calling commands and queries in a domain model.

Getting started
---------------

::

  # In your calling module
  from minty.cqrs import CQRS
  from minty.infrastructure import InfrastructureFactory
  from zsnl_domains import some_domain

  # Configure a CQRS instance (config file type may be ".conf" or ".json")
  infra_factory = InfrastructureFactory("/etc/configfile.conf") 
  cqrs = CQRS([some_domain], infra_factory)

  # Params can also be pre-set by the command or query function:
  query_instance = cqrs.get_query_instance("some_domain", "context")

  query_instance.some_query()


More documentation
------------------

Please see the generated documentation via CI for more information about this
module and how to contribute in our online documentation. Open index.html
when you get there:
`Sphinx Docs <https://gitlab.com/minty-python/minty/-/jobs/artifacts/master/browse/tmp/docs?job=qa>`_


Contributing
------------

Please read `CONTRIBUTING.md <https://gitlab.com/minty-python/minty/blob/master/CONTRIBUTING.md>`_
for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use `SemVer <https://semver.org/>`_ for versioning. For the versions
available, see the
`tags on this repository <https://gitlab.com/minty-python/minty/tags/>`_

License
-------

Copyright (c) 2018, Minty Team and all persons listed in
`CONTRIBUTORS <https://gitlab.com/minty-python/minty/blob/master/CONTRIBUTORS>`_

This project is licensed under the EUPL, v1.2. See the
`EUPL-1.2.txt <https://gitlab.com/minty-python/minty/blob/master/LICENSE>`_
file for details.
