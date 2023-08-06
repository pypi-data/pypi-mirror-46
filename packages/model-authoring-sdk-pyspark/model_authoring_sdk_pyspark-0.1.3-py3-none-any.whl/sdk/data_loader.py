#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2019 Adobe
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Adobe and its suppliers, if any. The intellectual
# and technical concepts contained herein are proprietary to Adobe
# and its suppliers and are protected by all applicable intellectual
# property laws, including trade secret and copyright laws.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Adobe.
#####################################################################

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from abc import abstractmethod, ABCMeta


class DataLoader:
    """
        Abstract class for data loader
    """

    __metaclass__ = ABCMeta


    def __init__(self):
        """
        Empty constructor.
        """
        pass

    @abstractmethod
    def load(self, configProperties, spark):
        """
        Load and return dataset
        :param configProperties: Config properties
        :param spark: Spark session
        :return: DataFrame
        """
        pass