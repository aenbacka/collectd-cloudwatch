"""
CollectdCloudWatchPlugin plugin
"""
import cloudwatch.modules.collectd_integration.dataset as dataset
try:
    import collectd # this will be in python path when running from collectd
except:
    import cloudwatch.modules.collectd as collectd
import traceback

import cloudwatch.modules.configuration.confighelper as confighelper
import cloudwatch.modules.flusher as flush
import cloudwatch.modules.logger.logger as logger

_LOGGER = logger.get_logger(__name__)


def aws_init():
    """
    Collectd callback entry used to initialize plugin
    """
    try:
        config = confighelper.ConfigHelper()
        flusher = flush.Flusher(config_helper=config,  dataset_resolver=dataset.get_dataset_resolver())
        collectd.register_write(aws_write, data = flusher)
        _LOGGER.info('Initialization finished successfully.')
    except Exception as e:
        _LOGGER.error("Cannot initialize plugin. Cause: " + str(e) + "\n" + traceback.format_exc())


def aws_write(vl, flusher):
    """ 
    Collectd callback entry used to write metric data
    """
    flusher.add_metric(vl)


collectd.register_init(aws_init)
