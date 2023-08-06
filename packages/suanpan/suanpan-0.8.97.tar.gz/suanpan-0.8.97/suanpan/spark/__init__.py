# coding=utf-8
from __future__ import absolute_import, print_function

from contextlib import contextmanager

from pyspark.sql import SparkSession

from suanpan import interfaces, objects
from suanpan.components import Component
from suanpan.log import logger


class SparkComponent(Component, interfaces.HasLogger):
    @contextmanager
    def context(self, args=None):  # pylint: disable=unused-argument
        spark = (
            SparkSession.builder.appName(self.runFunc.__name__)
            .enableHiveSupport()
            .getOrCreate()
        )
        yield objects.Context.froms(spark=spark)
        spark.stop()

    def beforeInit(self):
        logger.logDebugInfo()
        logger.debug("SparkComponent {} starting...".format(self.name))

    def initBase(self, args):
        logger.setLogger(self.name)

    def afterSave(self):
        logger.debug("SparkComponent {} done.".format(self.name))
