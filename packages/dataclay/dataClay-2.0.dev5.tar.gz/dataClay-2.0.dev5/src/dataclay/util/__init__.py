
""" Class description goes here. """

from datetime import datetime
from dataclay.util.ConfigurationFlags import ConfigurationFlags
import logging
import os
logger = logging.getLogger('dataclay.api')


class Configuration(object):
    """Configuration management static-ish class."""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    # Session control
    ########################
    CHECK_SESSION = False

    # Garbage collector
    ########################

    # Percentage to start flushing objects
    MEMMGMT_PRESSURE_FRACTION = 0.75

    # Number of milliseconds to check if Heap needs to be cleaned.
    MEMMGMT_CHECK_TIME_INTERVAL = 5000

    # Global GC collection interval
    NOCHECK_SESSION_EXPIRATION = datetime.strptime('2120-09-10T20:00:04', DATE_FORMAT)

    @classmethod
    def read_from_file(cls):
        # Check if environment variable is set 
        if "DATACLAYGLOBALCONFIG" in os.environ:
            flags_path = os.environ["DATACLAYGLOBALCONFIG"]
        else:
            flags_path = "./cfgfiles/global.properties"
        
        logger.info("Using global.properties at %s" % flags_path)
        try:
            flags = ConfigurationFlags(property_path=flags_path)
            if hasattr(flags, 'CHECK_SESSION'):
                logger.info("Found global.properties variable CHECKSESSION=%s" % flags.CHECK_SESSION)
                cls.CHECK_SESSION = eval(flags.CHECK_SESSION)
            if hasattr(flags, 'NOCHECK_SESSION_EXPIRATION'):
                logger.info("Found global.properties variable NOCHECK_SESSION_EXPIRATION=%s" % flags.NOCHECK_SESSION_EXPIRATION)
                cls.NOCHECK_SESSION_EXPIRATION = datetime.strptime(flags.NOCHECK_SESSION_EXPIRATION, cls.DATE_FORMAT)
            if hasattr(flags, 'MEMMGMT_PRESSURE_FRACTION'):
                logger.info("Found global.properties variable MEMMGMT_PRESSURE_FRACTION=%s" % flags.MEMMGMT_PRESSURE_FRACTION)
                cls.MEMMGMT_PRESSURE_FRACTION = float(flags.MEMMGMT_PRESSURE_FRACTION)
            if hasattr(flags, 'MEMMGMT_CHECK_TIME_INTERVAL'):
                logger.info("Found global.properties variable MEMMGMT_CHECK_TIME_INTERVAL=%s" % flags.MEMMGMT_CHECK_TIME_INTERVAL)
                cls.MEMMGMT_CHECK_TIME_INTERVAL = int(flags.MEMMGMT_CHECK_TIME_INTERVAL)
        except:
            logger.info("No global.properties file found. Using default values")


Configuration.read_from_file()
