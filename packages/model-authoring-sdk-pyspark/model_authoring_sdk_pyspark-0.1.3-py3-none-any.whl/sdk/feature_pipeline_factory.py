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


class FeaturePipelineFactory:
    """
        Abstract class for pipeline
    """

    __metaclass__ = ABCMeta


    def __init__(self):
        """
        Empty constructor.
        """
        pass

    @abstractmethod
    def create_pipeline(self, configProperties):
        """
        Create Spark pipeline.
        :param configProperties: Config properties
        :return: spark pipeline
        """
        pass

    @abstractmethod
    def get_param_map(self, configProperties, sparkSession):
        """
        Get param map from config properties.
        :param configProperties: Config properties
        :param sparkSession: Spark seesion
        :return: a param map
        """
        pass


    def set_data_transformer(self, data_transformer):
        """
        Set the internal data transformer.
        :param data_transformer: The pass in data transformer.
        """
        self.data_transformer = data_transformer


    def save(self, configProperties, dataframe):
        """
        Save dataframe.
        :param configProperties: Config properties
        :param dataframe: Dataframe
        """
        pass