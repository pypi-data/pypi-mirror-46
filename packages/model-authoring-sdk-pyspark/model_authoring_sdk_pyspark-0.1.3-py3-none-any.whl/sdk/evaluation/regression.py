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

from pyspark.sql.functions import col, avg, sqrt, abs, pow, lit
from sdk.mlevaluator import MLEvaluator
from sdk.util import Constants

class RegressionEvaluator(MLEvaluator):

    def __init__(self):
       print ("Initiate")

    def evaluate(self, data, model, configProperties):
        print ("Default Regression Evaluation triggered")

        if data is None :
            raise ValueError("Dataframe parameter is null")
        if model is None:
            raise ValueError("Model parameter is null")
        if configProperties is None:
            raise ValueError("configProperties parameter is null")

        if configProperties.get(Constants.LABEL_COL) is not None:
            label_column = configProperties.get(Constants.LABEL_COL)
        else :
            label_column = Constants.DEFAULT_LABEL
        if configProperties.get(Constants.SCALED_COL) is not None:
            scaled_column = configProperties.get(Constants.SCALED_COL)
        else :
            scaled_column = Constants.DEFAULT_SCALED
        if configProperties.get(Constants.PREDICT_COL) is not None:
            predict_column = configProperties.get(Constants.PREDICT_COL)
        else :
            predict_column = Constants.DEFAULT_PREDICT

        df = model.transform(data)
        df = df.withColumn("Residual", df[label_column] - df[predict_column])
        df = df.withColumn("AbsValueOfResidual", abs(df.Residual))

        df = df.withColumn("FirstDiff", df[scaled_column] - df[label_column])
        df = df.withColumn("AbsValueOfFirstDiff", abs(df.FirstDiff))

        df = df.withColumn("forMAPE", df["AbsValueOfResidual"]/df[label_column])

        if configProperties.get(Constants.METRIC_LIST) is not None:
            metrics_label_list = configProperties.get(Constants.METRIC_LIST).split(",")
        else :
            metrics_label_list = Constants.DEFAULT_REGRESSION_METRICS_LIST.split(",")

        metric = []
        for metric_label in metrics_label_list:
            if metric_label.strip().upper() == "MAE":
                mae = df.select(avg("AbsValueOfResidual")).rdd.flatMap(list).first()
                metric.append({"name": "MAE", "value": mae, "valueType": "double"})
            elif metric_label.strip().upper() == "MASE":
                mase = df.select(avg("AbsValueOfResidual")/avg("AbsValueOfFirstDiff")).rdd.flatMap(list).first()
                metric.append({"name": "MASE", "value": mase, "valueType": "double"})
            elif metric_label.strip().upper() == "RMSE":
                rmse = df.select(sqrt(avg(pow(df.AbsValueOfResidual, 2)))).rdd.flatMap(list).first()
                metric.append({"name": "RMSE", "value": rmse, "valueType": "double"})
            elif metric_label.strip().upper() == "MAPE":
                mape = df.select(avg("forMAPE")).rdd.flatMap(list).first()
                metric.append({"name": "MAPE", "value": mape, "valueType": "double"})
        return metric


    def split(self, configProperties, dataframe):

        if configProperties is None :
            raise ValueError("Config properties is not defined")
        if dataframe is None:
            raise ValueError("Dataframe is not defined")

        test_ratio = 0.2

        train_ratio_param = float(configProperties[Constants.TRAIN_RATIO])
        if (train_ratio_param is not None):
            if (0 <= train_ratio_param <= 1):
                test_ratio = 1 - train_ratio_param
            else:
                raise ValueError("Config parameter train_ratio is not in valid range [0, 1]")

        print("train_ratio is ", train_ratio_param)
        print("test_ratio is ", test_ratio)
        train, test = dataframe.randomSplit([train_ratio_param, test_ratio])

        return train, test
