# Configuration

The Pacifica Core services require two configuration files. The REST
API utilizes [CherryPy](https://github.com/cherrypy) and review of
their
[configuration documentation](http://docs.cherrypy.org/en/latest/config.html)
is recommended. The service configuration file is a INI formatted
file containing configuration for database connections.

## CherryPy Configuration File

An example of Ingest server CherryPy configuration:

```ini
[global]
log.screen: True
log.access_file: 'access.log'
log.error_file: 'error.log'
server.socket_host: '0.0.0.0'
server.socket_port: 8066

[/]
request.dispatch: cherrypy.dispatch.MethodDispatcher()
tools.response_headers.on: True
tools.response_headers.headers: [('Content-Type', 'application/json')]
```

## Service Configuration File

The service configuration is an INI file and an example is as follows:

```ini
[ingest]
; This section is specific to the ingest processes

; Local directory for incoming data and metadata
volume_path = /tmp

[uniqueid]
; This section describes where the UniqueID service is

; URL to the endpoint
url = http://127.0.0.1:8051

[policy]
; This section describes what endpoints are on the policy service

; Ingest URL to verify metadata
ingest_url = http://127.0.0.1:8181/ingest

[archiveinterface]
; This section describes where the archive interface is

; URL to the endpoint
url = http://127.0.0.1:8080

[metadata]
; This section describes what endpoints are on the metadata service

; Ingest URL for ingest metadata
ingest_url = http://127.0.0.1:8121/ingest

[celery]
; This section contains celery messaging configuration

; The broker url is how messages get passed around
broker_url = pyamqp://

; The backend url is how return results are sent around
backend_url = rpc://

[database]
; This section contains database connection configuration

; peewee_url is defined as the URL PeeWee can consume.
; http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url
peewee_url = sqliteext:///db.sqlite3

; connect_attempts are the number of times the service will attempt to
; connect to the database if unavailable.
connect_attempts = 10

; connect_wait are the number of seconds the service will wait between
; connection attempts until a successful connection to the database.
connect_wait = 20
```

## Starting the Service

Starting the Ingest service can be done by two methods. However,
understanding the requirements and how they apply to REST services
is important to address as well. Using the
internal CherryPy server to start the service is recommended for
Windows platforms. For Linux/Mac platforms it is recommended to
deploy the service with
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

### Deployment Considerations

The Ingest service is more critical for uploaders than the rest of
the Pacifica Core services. This is the first service that must be
put on the edge of your infrastructure and closest to where you are
getting your data from.

### CherryPy Server

To make running the Ingest service using the CherryPy's builtin
server easier we have a command line entry point.

```
$ pacifica-ingest --help
usage: pacifica-ingest [-h] [--cp-config CPCONFIG] [-c CONFIG] [-p PORT]
                       [-a ADDRESS]

Run the cart server.

optional arguments:
  -h, --help            show this help message and exit
  --cp-config CPCONFIG  cherrypy config file
  -c CONFIG, --config CONFIG
                        ingest config file
  -p PORT, --port PORT  port to listen on
  -a ADDRESS, --address ADDRESS
                        address to listen on
$ pacifica-ingest-cmd dbsync
$ pacifica-ingest
[09/Jan/2019:09:17:26] ENGINE Listening for SIGTERM.
[09/Jan/2019:09:17:26] ENGINE Bus STARTING
[09/Jan/2019:09:17:26] ENGINE Set handler for console events.
[09/Jan/2019:09:17:26] ENGINE Started monitor thread 'Autoreloader'.
[09/Jan/2019:09:17:26] ENGINE Serving on http://0.0.0.0:8066
[09/Jan/2019:09:17:26] ENGINE Bus STARTED
```

### uWSGI Server

To make running the Ingest service using uWSGI easier we have a
module to be included as part of the uWSGI configuration. uWSGI is
very configurable and can use this module many different ways. Please
consult the
[uWSGI Configuration](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html)
documentation for more complicated deployments.

```
$ pip install uwsgi
$ uwsgi --http-socket :8066 --master --module pacifica.ingest.wsgi
```
