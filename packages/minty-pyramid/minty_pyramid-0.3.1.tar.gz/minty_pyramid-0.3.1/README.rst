.. _readme:

Introduction
============

Pyramid configuration library Minty Python (micro)services.

Getting started
---------------
View::

  def hello(request):
    # See minty package for more information about these domain classes:
    domain_query_instance = request.get_query_instance("YourDomainHere")
    return domain_query_instance.some_domain_query()

Main::

  def main(*args, **kwargs):
    # See minty package for more information about these domain classes:
    loader = minty_pyramid.Engine(domains=[YourDomainHere])
   
    # [optional] To retrieve session information, make sure  to add before 
    # running loader.setup()
    kwargs["session_manager"] = True 

    # Ensure the "get_query_instance" request method is available
    # It will use a CQRS instance, built with an InstanceConfig built from
    # the configuration file specified in the file pointed to by
    # "minty_service.infrastructure.config_file" in kwargs
    config = loader.setup(*args, **kwargs)

    config.add_route("hello_world", "/hello")
    config.add_view(
        hello, request_method="GET", renderer="json", route_name="hello_world"
        )

    # If you've created the app from an openapi-spec file make sure to add: 
    routes.add_routes(config)

    # Returns a WSGI application
    return loader.main()
    

Code generation commands:
  generate-views: create boilerplate views by using "generate-views" command.
    When creating your application from an openapi(v3) spec file run
    "generate-views" to create "views.py" file with boilerplate code for all the views
    specified in the openapi spec.

    see "generate-views --help" for more info

  generate-routes: create Routes by using "generate-routes" command.
    Generate or re-generate "routes.py" file from an openapi spec file.

    see "generate-routes --help" for more info


More documentation
------------------

Please see the generated documentation via CI for more information about this
module and how to contribute in our online documentation. Open index.html
when you get there:
`<https://gitlab.com/minty-python/minty-pyramid/-/jobs/artifacts/master/browse/tmp/docs?job=qa>`_


Contributing
------------

Please read `CONTRIBUTING.md <https://gitlab.com/minty-python/minty-pyramid/blob/master/CONTRIBUTING.md>`_
for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use `SemVer <https://semver.org/>`_ for versioning. For the versions
available, see the
`tags on this repository <https://gitlab.com/minty-python/minty-pyramid/tags/>`_

License
-------

Copyright (c) 2018, Minty Team and all persons listed in
`CONTRIBUTORS <https://gitlab.com/minty-python/minty-cqs/blob/master/CONTRIBUTORS>`_

This project is licensed under the EUPL, v1.2. See the
`EUPL-1.2.txt <https://gitlab.com/minty-python/minty-pyramid/blob/master/LICENSE>`_
file for details.
