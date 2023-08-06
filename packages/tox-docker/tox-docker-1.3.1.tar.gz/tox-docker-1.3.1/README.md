# tox-docker 

A [tox](https://tox.readthedocs.io/en/latest/) plugin which runs one or
more [Docker](https://www.docker.com/) containers during the test run.

[![build status](https://travis-ci.org/tox-dev/tox-docker.svg?branch=master)](https://travis-ci.org/tox-dev/tox-docker)

## Usage and Installation

Tox loads all plugins automatically. It is recommended that you install the
tox-docker plugin into the same Python environment as you install tox into,
whether that's a virtualenv, etc.

You do not need to do anything special when running tox to invoke
tox-docker. You do need to configure your project to request docker
instances (see "Configuration" below).

## Configuration

In the `testenv` section, list the Docker images you want to include in
the `docker` multi-line-list. Be sure to include the version tag.

You can include environment variables to be passed to the docker container
via the `dockerenv` multi-line list. These will also be made available to
your test suite as it runs, as ordinary environment variables:

    [testenv]
    docker =
        postgres:9-alpine
    dockerenv =
        POSTGRES_USER=username
        POSTGRES_DB=dbname

## Host and Port Mapping

tox-docker runs docker with the "publish all ports" option. Any port the
container exposes will be made available to your test suite via environment
variables of the form `<image-basename>_<exposed-port>_<protocol>_PORT`. For
instance, for the postgresql container, there will be an environment
variable `POSTGRES_5432_TCP_PORT` whose value is the ephemeral port number
that docker has bound the container's port 5432 to.

Likewise, exposed UDP ports will have environment variables like
`TELEGRAF_8092_UDP_PORT` Since it's not possible to check whether UDP port
is open it's just mapping to environment variable without any checks that
service up and running.

The host name for each service is also exposed via environment as
`<image-basename>_HOST`, which is `POSTGRES_HOST` and `TELEGRAF_HOST` for
the two examples above.

*Deprecation Note:* In older versions of tox-docker, the port was exposed as
`<image-basename>-<exposed-port>-<protocol>`. This additional environment
variable is deprecated, but will be supported until tox-docker 2.0.
