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


class PipelineFactory:
    """
        Abstract class for creating Spark pipeline
    """

    __metaclass__ = ABCMeta


    def __init__(self):
        """
        Empty constructor
        """
        pass

    @abstractmethod
    def apply(self, configProperties):
        """
        Create Spark pipeline
        :param configProperties: Config properties
        :return: spark pipeline
        """
        pass

    @abstractmethod
    def train(self, configProperties, dataframe):
        """
        Train a custom pipeline that is not a Spark Pipeline.
        This method is not required when using Spark Pipeline.
        :param configProperties: Config properties
        :param dataframe: Feature dataset
        :return: custom training pipeline
        """
        pass

    @abstractmethod
    def score(self, configProperties, dataframe, model):
        """
        Perform scoring on test data using a custom pipeline that is not a Spark Pipeline.
        This method is not required when using Spark Pipeline.
        :param configProperties: Config properties
        :param dataframe: Test dataset
        :param model: A trained model
        :return: prediction results
        """
        pass

    @abstractmethod
    def get_param_map(self, configProperties, sparkSession):
        """
        Get param map from config properties
        :param configProperties: Config properties
        :param sparkSession: Spark seesion
        :return: a param map
        """
        pass


    def save(self, configProperties, dataframe):
        """
        Save dataframe
        :param configProperties: Config properties
        :param dataframe: Dataframe
        """
        pass