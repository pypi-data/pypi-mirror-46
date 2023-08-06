#####################################################################
# ADOBE CONFIDENTIAL
# ___________________
#
#  Copyright 2018 Adobe
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
import numpy as np
from pyspark.mllib.evaluation import BinaryClassificationMetrics, MulticlassMetrics
from pyspark.sql.types import DoubleType
from sdk.mlevaluator import MLEvaluator
from sdk.util import Constants

class ClassificationEvaluator(MLEvaluator):

    def __init__(self):
        print("Initiate")

    def evaluate(data=[], model={}, configProperties={}):
        print ("Default Classification Evaluation triggered")

        if data is None :
            raise ValueError("Dataframe parameter is null")
        if model is None:
            raise ValueError("Model parameter is null")
        if configProperties is None:
            raise ValueError("configProperties parameter is null")

        if configProperties.get(Constants.LABEL_COL) is not None:
            label_col = configProperties.get(Constants.LABEL_COL)
        else:
            label_col = Constants.DEFAULT_LABEL
        if configProperties.get(Constants.PREDICT_COL) is not None:
            prediction_col = configProperties.get(Constants.PREDICT_COL)
        else:
            prediction_col = Constants.DEFAULT_PREDICT
        if configProperties.get(Constants.METRIC_LIST) is not None:
            metrics_label_list = configProperties.get(Constants.METRIC_LIST).split(",")
        else:
            metrics_label_list = Constants.DEFAULT_CLASSIFICATION_METRICS_LIST.split(",")

        predictions = model.transform(data)
        prediction_and_label = predictions.select(prediction_col, label_col)
        multi_class_metrics = MulticlassMetrics(prediction_and_label.rdd)
        metric = []

        for metric_label in metrics_label_list:
            if metric_label.strip().lower() == "precision":
                metric.append({"name": "precision", "value": str(multi_class_metrics.weightedPrecision),
                               "valueType": "double"})
            elif metric_label.strip().lower() == "recall":
                metric.append({"name": "recall", "value": str(multi_class_metrics.weightedRecall),
                               "valueType": "double"})
            elif metric_label.strip().lower() == "confusion matrix":
                confusion_matrix = multi_class_metrics.confusionMatrix().toArray()
                confusion_array = np.ravel(confusion_matrix)
                confusion_array = confusion_array.astype(int)
                metric.append({"name": "confusion matrix", "value": np.array2string(confusion_array, separator=','),
                               "valueType": "matrix"})
            elif metric_label.strip().lower() == "f-score":
                metric.append({"name": "f-score", "value": str(multi_class_metrics.weightedFMeasure()),
                               "valueType": "double"})
            elif metric_label.strip().lower() == "accuracy":
                metric.append({"name": "accuracy", "value": str(multi_class_metrics.accuracy), "valueType": "double"})
            elif metric_label.strip().lower() == "roc":
                fpr = multi_class_metrics.weightedFalsePositiveRate
                tpr = multi_class_metrics.weightedTruePositiveRate
                metric.append({"name": "roc", "value": str([(0.0, 0.0), (fpr, tpr), (1.0, 1.0), (1.0, 1.0)]),
                               "valueType": "chart"})
            elif metric_label.strip().lower() == "auroc":
                binary_classification_metrics = BinaryClassificationMetrics(prediction_and_label.rdd)
                metric.append({"name": "auroc", "value": str(binary_classification_metrics.areaUnderROC),
                               "valueType": "double"})

        return metric


    def split(configProperties={}, data={}):
        if configProperties is None:
            raise ValueError("Config properties is not defined")
        if data is None:
            raise ValueError("Dataframe is not defined")

        test_ratio = 0.2
        train_ratio_param = float(configProperties[Constants.TRAIN_RATIO])
        if train_ratio_param is not None:
            if 0 <= train_ratio_param <= 1:
                test_ratio = 1 - train_ratio_param
            else:
                raise ValueError("Config parameter train_ratio is not in valid range [0, 1]")

        print("train_ratio is ", train_ratio_param)
        print("test_ratio is ", test_ratio)
        train, test = data.randomSplit([train_ratio_param, test_ratio])

        return train, test



