# antares-client

A light-weight client for receiving alerts from
[ANTARES](http://antares.noao.edu).

ANTARES is an Alert Broker developed by the [NOAO](http://noao.edu) for ZTF and
LSST.

The client is available for use as a Python library and as a command line tool.
Directions for both use cases follow in the [Usage](#usage) section.

Table of Contents:
* [Installation](#installation)
* [Documentation](#documentation)
* [Upgrading](#upgrading)
* [Troubleshooting](#troubleshooting)

## Installation

The ANTARES client supports Python versions 3.4 and up. Python 2.X is not
supported.

You can install using `pip`:

```bash
$ pip install antares-client
```

Verify the client installed correctly:

```bash
$ antares --version
antares, version v0.3.0
```

## Documentation

Visit the [full documentation](https://noao.gitlab.io/antares/client) for usage
guides, API reference docs, and more.

## Version Migration

While the ANTARES client is still in beta (pre-1.0) we will likely make a
handful of breaking changes. This section will help ease your migratory pains.
Thank you for supporting us in our infancy!

### 0.2.x to 0.3.x

- The CLI command for streaming alerts from ANTARES, ``antares-client``, has
  been renamed ``antares stream``. Additionally, in 0.2.0 you were able to pass
  topics to ``antares-client`` in a comma-separated list--this functionality has
  been removed in favor of space-separated lists. So, for example, this 0.2.0
  call:

  ```
  antares-client extragalactic,nuclear_transient
  ```

  should be replaced with this 0.3.0 call:

  ```
  antares stream extragalactic nuclear_transient
  ```

## Troubleshooting

Issues? See the
[documentation](https://noao.gitlab.io/antares/client/troubleshooting) for
common gotchas and, if you can't find a solution there, please open an issue.

