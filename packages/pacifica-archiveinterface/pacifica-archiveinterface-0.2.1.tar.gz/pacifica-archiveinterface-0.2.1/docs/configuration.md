# Configuration

The configuration of the Archive Interface service is done in two
files. The REST API utilizes [CherryPy](https://github.com/cherrypy)
and review of their
[configuration documentation](http://docs.cherrypy.org/en/latest/config.html)
is recommended. The service configuration file is a INI formatted
file containing configuration for accessing the HSM backend.

## CherryPy Configuration File

An example of Archive Interface server CherryPy configuration:

```ini
[global]
log.screen: True
log.access_file: 'access.log'
log.error_file: 'error.log'
server.socket_host: '0.0.0.0'
server.socket_port: 8080

[/]
request.dispatch: cherrypy.dispatch.MethodDispatcher()
tools.response_headers.on: True
tools.response_headers.headers: [('Content-Type', 'application/json')]
```

## Service Configuration File

The service configuration is an INI file and an example is as follows:

```
[posix]
; use id2filename method when accessing a posix endpoint
use_id2filename = false

[hpss]
; IBM HPSS HSM settings
auth = /var/hpss/etc/hpss.unix.keytab
sitename = example.com
user = hpss.unix

[hsm_sideband]
; Oracle HSM Sideband database settings (MySQL)
sam_qfs_prefix = /tmp/path
schema = schema_name
host = host
user = user
password = pass
port = 3306
```

## ID Mapping to File Names

The Pacifica software depends on a flat ID space for indexing files. This needs
to map to filenames on the backend storage in a nice way. To limit the number of
files in a single directory (or number of directories in a directory) we use the
algorithm in `archiveinterface.id2filename`. This takes a number and breaks it
into bytes. Each byte is then represented in hex and used to build the directory
tree.

For example `id2filename(12345)` becomes `/39/3039` on the backend file system.

## Running It

There are two ways of running the archive interface, using CherryPy builtin
server and uWSGI to run the server.


[CherryPy](https://github.com/cherrypy) does provide a server and this works
for some workloads.

```
pacifica-archiveinterface -t posix -p 8080 -a 127.0.0.1 --prefix /path
```

[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) is recommended for this
service as it performs a lot better for higher throughput workloads.

```
export PAI_BACKEND_TYPE=posix
export PAI_PREFIX=/path
uwsgi --http-socket :8080 --master -p 8 --module pacifica.archiveinterface.wsgi
```

# Post Deployment Testing

Inside the `post_deployment_test` directory there is a file called `deployment_test.py`
This file will run a series of tests against a deployed archive interface.  The test
are ordered so that they post, stage, status, and get files properly.
There are a few global variables at the top of the file that need to be adjusted to each deployment.

## Variables

```
export ARCHIVE_URL='http://127.0.0.1:8080/'
```
 - ARCHIVE_URL is the URL to the newly deployed archive_interface

## Running

```
pytest -v post_deployment_tests/deployment_test.py
```

Output will be the status of the tests against the archive interface
