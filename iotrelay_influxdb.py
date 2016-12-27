'''
Copyright (c) 2016, Emmanuel Levijarvi
All rights reserved.
License BSD 2-Clause
'''
import logging
from collections import defaultdict
import influxdb
from influxdb.exceptions import InfluxDBServerError, InfluxDBClientError

logger = logging.getLogger(__name__)

__version__ = "1.7.0"

DEFAULT_BATCH_SIZE = 30
HOST = 'localhost'
USERNAME = 'root'
PASSWORD = 'root'
USE_SSL = 'False'
VERIFY_SSL = True
DATABASE = 'iotrelay'
INFLUXDB_PORT = 8086


class Handler(object):
    "An InfluxDB handler class implementing iotrelay callbacks"

    def __init__(self, config):
        """Construct an Influxdb handler, using the iotrelay-influxdb section
           in the iotrelay configuration file.
        """
        self.readings = defaultdict(list)
        self.config = config
        self.batch_size = int(config.get('batch size', DEFAULT_BATCH_SIZE))
        port = config.get('influx db port', INFLUXDB_PORT)
        use_ssl = config.get('use_ssl', USE_SSL) == "TRUE"
        host = config.get('host', HOST)
        username = config.get('username', USERNAME)
        password = config.get('password', PASSWORD)
        self.database = config.get('database', DATABASE)
        self.client = influxdb.InfluxDBClient(
            host, port, username, password, ssl=use_ssl, verify_ssl=VERIFY_SSL,
            timeout=2)

    def set_reading(self, reading):
        "Store a reading in the InfluxDB plugin."
        logger.debug('influxdb setting: %s', reading)
        points = self.readings[(reading.series_key, reading.reading_type)]
        point = {'measurement': reading.series_key, 'time': reading.timestamp,
                 'fields': {'value': reading.value}}
        if reading.tags:
            point['tags'] = reading.tags
        logger.debug('Received point: %s', point)
        points.append(point)
        batch_option = "{0} batch size".format(reading.reading_type)
        if len(points) >= int(self.config.get(batch_option, self.batch_size)):
            self.send_reading(reading.series_key, reading.reading_type, points)

    def flush(self):
        "Send any stored readings and empty the buffer."
        [self.send_reading(series[0], series[1], points)
         for series, points in self.readings.items()]

    def send_reading(self, series_key, reading_type, points):
        """When the number of stored readings is at or above the set batch size,
         send them to InfluxDB."""
        database_option_key = "{0} base".format(reading_type)
        database = self.config.get(database_option_key, self.database)
        db_list = self.client.get_list_database()
        if database not in [db['name'] for db in db_list]:
            logger.info('creating database: %s', database)
            try:
                self.client.create_database(database)
            except (InfluxDBServerError, InfluxDBClientError) as error:
                logger.exception(error)
        self.client.switch_database(database)
        logger.debug(points)
        logger.debug("write points: %s", points)
        try:
            self.client.write_points(points)
        except influxdb.exceptions.InfluxDBServerError as error:
            logger.error('Unable to send %s to InfluxDB.', series_key)
            logger.exception(error)
        else:
            del self.readings[(series_key, reading_type)]
