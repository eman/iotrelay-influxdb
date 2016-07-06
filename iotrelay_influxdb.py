'''
Copyright (c) 2016, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import logging
import calendar
from collections import defaultdict
import influxdb

logger = logging.getLogger(__name__)
__version__ = "1.3.0"
DEFAULT_BATCH_SIZE = 30
INFLUXDB_PORT = 8086


class Handler(object):
    def __init__(self, config):
        self.readings = defaultdict(list)
        self.config = config
        self.batch_size = int(config.get('batch size', DEFAULT_BATCH_SIZE))
        port = config.get('influx db port', INFLUXDB_PORT)
        host = config['host']
        username = config['username']
        password = config['password']
        self.database = config['database']
        self.client = influxdb.InfluxDBClient(host, port, username, password,
                                              timeout=2)

    def set_reading(self, reading):
        logger.debug('influxdb setting: {0!s}'.format(reading))
        points = self.readings[(reading.series_key, reading.reading_type)]
        timestamp = calendar.timegm(reading.timestamp.timetuple())
        points.append((timestamp, reading.value))
        batch_option = "{0} batch size".format(reading.reading_type)
        if len(points) >= int(self.config.get(batch_option, self.batch_size)):
            self.send_reading(reading.series_key, reading.reading_type, points)

    def flush(self):
        [self.send_reading(series[0], series[1], points)
         for series, points in self.readings.items()]

    def send_reading(self, series_key, reading_type, points):
        database_option_key = "{0} base".format(reading_type)
        database = self.config.get(database_option_key, self.database)
        db_list = self.client.get_list_database()
        if database not in [db['name'] for db in db_list]:
            logger.info('creating database: {0}'.format(database))
            try:
                self.client.create_database(database)
            except influxdb.exceptions.InfluxDBClientError as e:
                logger.exception(e)
        self.client.switch_database(database)
        logger.debug(points)
        series = {'name': database, 'columns': ['time', series_key],
                  'points': points}
        logger.debug("write series: {0!s}".format(series))
        try:
            self.client.write_points([series])
        except Exception as e:
            logger.error('Unable to send {0} to InfluxDB.'.format(series_key))
            logger.exception(e)
        else:
            del self.readings[(series_key, reading_type)]
