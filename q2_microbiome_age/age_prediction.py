# ----------------------------------------------------------------------------
# Copyright (c) 2020--, Shi Huang.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# Functions
import pandas as pd
import numpy as np
from biom import Table
import qiime2 as q2
from qiime2 import Artifact
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from qiime2.plugins.sample_classifier.actions import predict_regression, regress_samples, scatterplot

def _age_prediction_with_trained_model(q2_model, test_table, test_metadata):
    '''
    Predict age in the test microbiome dataset based on a trained model.
    Parameters
    ----------
    trained_model: qiime2.sample_estimator 
        A trained regression model generated by qiime2.sample-regressor
    test_table: A pd.DataFrame with test data
    test_metadata : qiime2.CategoricalMetadataColumn
        metadata column with samples labeled as "case" or "control".
        All samples with either label are returned, normalized to the
        equivalent percentile in "control" samples.
    Returns
    -------
    updated_test_metadata: A pd.DataFrame with an updated test metadata where
        microbiome age has been inerted into the last column.
    '''

    #q2_model=q2.Artifact.load(q2_model)
    predictions=predict_regression(q2_test_table, q2_model).predictions
    #predictions.save(OUTDIR+'test_predictions.qza')

    test_pred_df=predictions.view(pd.Series)
    updated_test_metadata = pd.concat([test_metadata, test_pred_df], axis=1, sort=False)
    #result.to_csv(OUTDIR+'test_predictions_metadata.tsv',sep='\t') 
    
    return updated_test_metadata

def age_prediction_with_trained_model(q2_model: qiime2.sample_estimator,
                                        test_table:biom.Table,
                                        test_metadata: qiime2.MetadataColumn) -> pd.DataFrame:
    '''
    Predict age in the test microbiome dataset based on a trained model.
    Parameters
    ----------
    trained_model: qiime2.sample_estimator 
        A trained regression model generated by qiime2.sample-regressor
    test_table: A pd.DataFrame with test data
    test_metadata : qiime2.CategoricalMetadataColumn
        metadata column with samples labeled as "case" or "control".
        All samples with either label are returned, normalized to the
        equivalent percentile in "control" samples.
    Returns
    -------
    test_df_padded: A pd.DataFrame with an updated test data with equal number of
        feature as the train data.
    '''

    #q2_model=q2.Artifact.load(q2_model)
    predictions=predict_regression(q2_test_table, q2_model).predictions
    #predictions.save(OUTDIR+'test_predictions.qza')

    test_pred_df=predictions.view(pd.Series)
    updated_test_metadata = pd.concat([test_metadata, test_pred_df], axis=1, sort=False)
    #result.to_csv(OUTDIR+'test_predictions_metadata.tsv',sep='\t') 
    
    return updated_test_metadata

def _age_prediction_with_train_data(train_table, train_metadata, train_target_field, test_table):
    '''
    Predict age in the test microbiome dataset based on a trained model.
    Parameters
    ----------
    model_fp: qiime2.sample_estimator 
        A trained regression model generated by qiime2.sample-regressor
    test_table: A pd.DataFrame with test data
    test_metadata : qiime2.CategoricalMetadataColumn
        metadata column with samples labeled as "case" or "control".
        All samples with either label are returned, normalized to the
        equivalent percentile in "control" samples.
    Returns
    -------
    updated_test_metadata: A pd.DataFrame with an updated test metadata where
        microbiome age has been inerted into the last column.
    '''
    try:
        train_y=train_metadata[train_target_field]
        except NameError:
            print("The train_target_field is not found!")
    train_table_q2 = Artifact.import_data("FeatureTable[Frequency]", train_table)
    train_metadata_q2 = q2.Metadata(train_metadata) # q2 metadata
    train_y_q2=train_metadata_q2.get_column(train_target_field)

    test_table_q2 = Artifact.import_data("FeatureTable[Frequency]", test_table)
    test_metadata_q2 = q2.Metadata(test_metadata) # q2 metadata
    out = regress_samples(q2_train_X, q2_train_y, cv=5, n_jobs=8, n_estimators=500, parameter_tuning=False)
    q2_model = out.sample_estimator

    predictions=predict_regression(test_table_q2, q2_model).predictions
    #predictions.save(OUTDIR+'test_predictions.qza')

    test_pred_df=predictions.view(pd.Series)

    updated_test_metadata = pd.concat([test_metadata, test_pred_df], axis=1, sort=False)
    #result.to_csv(OUTDIR+'test_predictions_metadata.tsv',sep='\t') 
    
    return updated_test_metadata

def age_prediction_with_train_data(train_table: biom.Table, 
                                    train_metadata:qiime2.Metadata, 
                                    train_target_field:str,
                                    test_table:biom.Table, 
                                    test_metadata: qiime2.metadata,
                                    n_jobs_or_threads: int = 4,
                                    cv: int = 5,
                                    n_estimators: int = 500,
                                    parameter_tuning: bool = False) -> pd.DataFrame:
    '''
    Predict age in the test microbiome dataset based on a trained model.
    Parameters
    ----------
    train_table: biom.Table
        Feature table with relative abundances for model training. Samples are in columns,
        features (i.e. OTUs) are in rows.
    train_metadata : qiime2.MetadataColumn
        metadata column with samples labeled as age values ranging from 0 to 120.
    test_table: Feature table with relative abundances for model testing. Samples are in columns,
        features (i.e. OTUs) are in rows.
    test_metadata : qiime2.MetadataColumn
        metadata column with samples labeled as age values ranging from 0 to 120.
    Returns
    -------
    updated_test_metadata: A pd.DataFrame with an updated test metadata where
        microbiome age has been inerted into the last column.
    '''
    
    # Filter metadata to only include IDs present in the table.
    # Also ensures every distance table ID is present in the metadata.
    train_metadata = train_metadata.filter_ids(train_table.ids(axis='sample'))
    train_metadata = train_metadata.drop_missing_values() 
    # filter sample IDs with missing values in the train_table
    train_table = train_table.filter(metadata.ids) 

    train_table_q2 = Artifact.import_data("FeatureTable[Frequency]", train_table)
    train_metadata_q2 = q2.Metadata(train_metadata) # q2 metadata
    train_y_q2=train_metadata_q2.get_column(train_target_field)

    
    # train the model with q2-sample-classifier
    out = regress_samples(q2_train_X, q2_train_y, cv=cv, n_jobs=n_jobs_or_threads, n_estimators=n_estimators, parameter_tuning=parameter_tuning)
    q2_model = out.sample_estimator

    # age prediction in the test table 
    test_table_q2 = Artifact.import_data("FeatureTable[Frequency]", test_table)
    #test_metadata_q2 = q2.Metadata(test_metadata) # q2 metadata
    predictions=predict_regression(test_table_q2, q2_model).predictions
    #predictions.save(OUTDIR+'test_predictions.qza')

    test_pred_df=predictions.view(pd.Series)

    updated_test_metadata = pd.concat([test_metadata, test_pred_df], axis=1, sort=False)
    #result.to_csv(OUTDIR+'test_predictions_metadata.tsv',sep='\t') 
    
    return updated_test_metadata


