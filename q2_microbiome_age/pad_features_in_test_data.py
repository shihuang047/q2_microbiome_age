# ----------------------------------------------------------------------------
# Copyright (c) 2020--, Shi Huang.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

# Data types or functions
import biom
import pandas as pd
import numpy as np


def _pad_features_in_test_data(train_df, test_df):
    '''
    Do feature alignment on two dataframes.
    Parameters
    ----------
    train_df: A pd.DataFrame with train data
    test_df: A pd.DataFrame with test data
    Returns
    -------
    new_test_df: A pd.DataFrame with an updated test data with equal number of
        feature as the train data.
    '''
    #train_df=train_data.view(pd.DataFrame)
    #test_df=test_data.view(pd.DataFrame)
    train_feature_ids=train_df.columns.values.tolist()
    test_feature_ids=test_df.columns.values.tolist()
    #print("The # of features in the train data: ", len(train_feature_ids))
    #print("The # of features in the original test data: ", len(test_feature_ids))
    train_uniq_f=list(set(train_feature_ids)-set(test_feature_ids))
    shared_f=set(train_feature_ids).intersection(set(test_feature_ids))
    #print("The # of features with all zeros in the new test data: ", len(train_uniq_f))
    #print("The # of shared features kept in the new test data: ", len(shared_f))
    test_padding_matrix = pd.DataFrame(0, index=test_df.index, columns=train_uniq_f)
    new_test_df=pd.concat([test_df[shared_f], test_padding_matrix], axis=1)
    new_test_df=new_test_df[train_feature_ids]    
    print("The shape of new test data: ", new_test_df.shape)
    #new_test_df_qza=q2.Artifact.import_data('FeatureTable[Frequency]', new_test_df)
    return new_test_df

def pad_features_in_test_data(train_table: biom.Table, test_table: biom.Table) -> biom.Table:
    '''
    Do feature alignment on train and test tables by adding zero-padding features that
    only existed in the train table into test table.

    Parameters
    ----------
    train_table: biom.Table
    A biom table with train data
    test_table: biom.Table
    A biom table with test data
    
    Returns
    -------
    new_test_biom: biom.Table
    A biom table with the updated test data with identical set of
        features in the train table.
    '''
    
    train_feature_ids = train_table.ids(axis='observation')
    test_feature_ids = test_table.ids(axis='observation')
    n_samples = test_table.shape[0]
    sample_ids= test_table.ids(axis='sample')
    #print("The # of features in the train data: ", len(train_feature_ids))
    #print("The # of features in the original test data: ", len(test_feature_ids))
    train_uniq_f=list(set(train_feature_ids)-set(test_feature_ids))
    shared_f=set(train_feature_ids).intersection(set(test_feature_ids))
    # create a zero matrix for all features uniquely existed in the train table
    padding_table = biom.Table(np.zeros((len(train_uniq_f), n_samples)),
                                train_uniq_f, sample_ids)
    # filter out features that don't exist in the train table in the test table
    test_table.filter(shared_f, axis='observation')
    # merge the two tables
    new_test_table = test_table.merge(padding_table)

    return new_test_table


