IoT Relay - InfluxDB
----------------------------------------------------------------------------
version 1.5.1

iotrelay-influxdb is a data handler plugin for IoT Relay. It watches for
data it has registered an interest in and relays it in batches to a
InfluxDB time series database. See the `IoT Relay Documentation
<https://github.com/eman/iotrelay>`_ for more.

iotrelay-influxdb is available on PyPI and can be installed via pip.

.. code-block:: bash

    $ pip install iotrelay-influxdb

Before using iotrelay-influxdb a database must be
created. See https://influxdb.com/ for more.
to the IOT Relay configuration file, ``~/.iotrelay.cfg`` once they have
been given by InfluxDB.

.. code-block:: ini

    [iotrelay-influxdb]
    host = influxdb hostname
    username = influxdb password
    password = influxdb password

The ``reading types`` to be relayed to InfluxDB should also be
registered. In this example, reading types of power and weather will be
relayed to InfluxDB.

.. code-block:: ini

    [iotrelay-influxdb]
    reading types = power, weather
    host = influxdb hostname
    username = influxdb username
    password = influxdb password

By default iotrelay-influxdb will batch 30 readings of each type before
sending the batch to InfluxDB. In the previous example, two separate
batches would be maintained for power and weather readings. The batch
size may be changed by adding the ``batch size`` option to the
``iotrelay-influx`` section of ``~/.iotrelay.cfg``.

.. code-block:: ini

    [iotrelay-influxdb]
    batch size = 30
    reading types = power, weather
    host = influxdb hostname
    username = influxdb username
    password = influxdb password
