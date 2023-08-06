'''
 * ADOBE CONFIDENTIAL
 * ___________________
 *
 *  Copyright 2019 Adobe Systems Incorporated
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Adobe Systems Incorporated and its suppliers,
 * if any.  The intellectual and technical concepts contained
 * herein are proprietary to Adobe Systems Incorporated and its
 * suppliers and are protected by all applicable intellectual property
 * laws, including trade secret and copyright laws.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Adobe Systems Incorporated.
'''
#Constants
METRIC_LIST = "evaluation.metrics"
DEFAULT_REGRESSION_METRICS_LIST = "MAPE,MAE,RMSE,MASE"
DEFAULT_CLASSIFICATION_METRICS_LIST = "precision, recall, confusion matrix, f-score, accuracy, roc, auroc"
LABEL_COL = "evaluation.labelColumn"
SCALED_COL = "evaluation.scalingColumn"
PREDICT_COL = "evaluation.predictionColumn"
DEFAULT_LABEL = "label"
DEFAULT_SCALED = "scaled"
DEFAULT_PREDICT = "prediction"
TRAIN_RATIO = "evaluation.trainRatio"
SEED = "evaluation.seed"

