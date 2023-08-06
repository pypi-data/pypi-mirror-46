# antares-client

A light-weight client for receiving alerts from
[ANTARES](http://antares.noao.edu).

ANTARES is an Alert Broker developed by the [NOAO](http://noao.edu) for ZTF and
LSST.

The client is available for use as a Python library and as a command line tool.
Directions for both use cases follow in the [Usage](#usage) section.

Table of Contents:
* [Credentials](#credentials)
* [Installation](#installation)
* [Usage](#usage)
  - [As a Command Line Tool](#as-a-command-line-tool)
  - [As a Library](#as-a-library)
* [Troubleshooting](#troubleshooting)

## Credentials

You'll need to contact the ANTARES team to request API credentials.

These credentials are different than your sign-in credentials for
`antares.noao.edu`. We typically grant only one set of credentials per
institution. If approved, you will recieve a set of credentials: an API Key and
an API Secret. Do not share these credentials with others. We request that you
operate only one active consumer per set of credentials, except with the
permission of the NOAO.

The NOAO reserves the right to monitor your usage and revoke your credentials at
any time.

## Installation

The `antares-client` supports Python versions 3.4 and up. Python 2.X is not
supported.

You can install using `pip`:

```bash
pip install antares-client
```

Verify the client installed correctly:

```bash
antares-client --version
```

## Usage

This section contains instructions for using the ANTARES client both [as a
command line tool](#as-a-command-line-tool) and [as a library](#as-a-library).


### As a Command Line Tool

The `antares-client` command line interface (CLI) serves a single purpose. It
subscribes to ANTARES streams and writes alerts to `*.json` files in a directory
of your choice. For more advanced use-cases, see [using the ANTARES client as a
library](#as-a-library).

For example, to save all alerts from the `extragalactic` stream to a folder in
your home directory called `antares/extragalactic`:

```bash
antares-client extragalactic \
  --output-directory ~/antares
  --api-key ********************
  --api-secret ********************
```

The client creates a subdirectory in `--output-directory` named after the stream
you're subscribing to and saves that stream's alerts there (in this case,
`~/antares/extragalactic`).

You can also subscribe to multiple streams:

```bash
antares-client extragalactic,nuclear_transient \
  --output-directory ~/antares
  --api-key ********************
  --api-secret ********************
```

And this will save the alerts from the `extragalactic` and `nuclear_transient`
streams in `~/antares/extragalactic` and `~/antares/nuclear_transient`,
respectively.

### As a Library

The ANTARES client can be used in other Python code. The `antares_client.Client`
object exposes an interface for subscribing to and retrieving alerts from
ANTARES' streams. Before presenting the [API reference](#api-reference) for this
object, here is a example that shows how to subscribe to the `extragalactic`
stream:

```python
from antares_client import Client


def main():
    # The client is instantiated; though there are more options that can be 
    # passed to the constructor, the `topics` argument and the `api_key` and
    # `api_secret` keyword arguments are required.
    client = Client(
        topics=["extragalactic"],
        api_key="********************",
        api_secret="********************",
    )

    while True:
        # The `Client.poll` method will block until an alert is available.
        # The returned `alert` is a dictionary.
        topic, alert = client.poll()
        do_something(alert)

    # We must close our connection to ANTARES when we are done with it.
    client.close()


if __name__ == "__main__":
    main()
```

#### API Reference

##### `Client`

The `antares_client.Client` object exposes the `Client.poll` method for
retrieving alerts from ANTARES.

###### `Client.poll(timeout=-1)`

This method returns a `(topic, alert)` tuple. If `timeout` seconds elapse and
no alerts are available it will return `(None, None)`. By default, `poll` will
wait indefinitley for an alert.

###### `Client.iter(num_alerts=None)`

This method returns an iterator over `(topic, alert)` tuples from the streams
the client is subscribed to. By default it will iterate indefinitly; passing an
integer value to the `num_alerts` keyword argument will force the iterator to
break after fetching that many alerts.

###### `Client.close`

This method closes the client's connection to its ANTARES streams.

###### Context Management

We also provide the ability to use a `Client` instance as a context manager.
For example, this code:

```python
config = {
    "api_key"="********************",
    "api_secret"="********************",
}

with Client(["extragalactic"], **config) as client:
    for topic, alert in client.iter():
        do_something(alert)
```

Is more concise than its expanded form:

```python
config = {
    "api_key"="********************",
    "api_secret"="********************",
}

client = Client(["extragalactic"], **config)
try:
    while True:
        topic, alert = client.poll()
        do_something(alert)
finally:
    client.close()
```

#### Downloading image thumbnails

ANTARES stores ZTF image thumbnails for all alerts which we store or stream
out. You can retrieve these thumbnails using the antares_client like so:

```python
>>> from antares_client.thumbnails import get_thumbnails
>>>
>>> alert_id = 9898524
>>> thumbnails = get_thumbnails(alert_id)
>>> print(thumbnails)
{
    'template': {
        'file_name': '...fits.gz',
        'file_bytes': '...'
    },
    'science': {
        'file_name': '...fits.gz',
        'file_bytes': '...'
    },
    'difference': {
        'file_name': '...fits.gz',
        'file_bytes': '...'
    }
}
>>>
>>> # You can also have them saved to a directory for you.
>>> # The return value is the same as before.
>>> alert_id = 9898524
>>> output_dir = "/foo/bar/thumbnails/"  # Your output directory
>>> thumbnails = get_thumbnails(alert_id, output_dir)
>>>
```

## Troubleshooting

### A Note About Subscriptions (and Kafka Commits)

ANTARES remembers which alerts you have or have not received. If you start
consuming alerts, stop and resume later, you will pick up where you left off.
Kafka provides the underlying functionality for ANTARES so, in Kafka-terms:
message offsets are automatically committed every 5 seconds.

### "Could not locate SSL certificates"

Connecting to ANTARES requires SSL certificates. The client will attempt to
find them automatically but there is a chance it may fail. If this happens,
you'll see an error message like "Could not locate SSL certificates".

You will need to manually locate your SSL certificates and pass their path
to the ANTARES client. Run the following command to see which directory
`openssl` is configured to look for certificates in:

```bash
openssl version -d
```

Look in the output directory for your certificates file--usually named
`certs.pem` or `ca-certificates.crt`. If you are using anaconda or miniconda, it
may be something like `.../miniconda/ssl/cert.pem`.

If you are using the client as a command line tool, pass the option
`--ssl-ca-location /path/to/your/cert/file`. If you are using the client as a
library, pass the `ssl_ca_location` keyword argument to the `Client` constructor
(e.g. `Client(..., ssl_ca_location="path/to/your/cert/file", ...)`).

### Logging messages

During normal operations, the client may lose its connection to ANTARES. When
this happens it will automatically attempt to reconnect. When this occurs, the
client wil continue to operate normally but you may see messages like:

```
%3|1544735845.925|FAIL|rdkafka#consumer-1|
[thrd:sasl_ssl://b0-pkc-epgnk.us-central1.gcp.confluent.cloud:9092/0]:
sasl_ssl://b0-pkc-epgnk.us-central1.gcp.confluent.cloud:9092/0: Disconnected
(after 600053ms in state UP)
```

Don't worry, this is normal!
