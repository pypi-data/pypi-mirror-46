import pandas as pd
from pyspark.sql import DataFrame
from pyspark.mllib.stat import Statistics

def spark_corr_matrix(df: DataFrame, method: str="pearson", dropna: bool=True) -> pd.DataFrame:
    """
    Computes correlation matrix between all columns in a spark DataFrame
    :param df: Spark DataFrame
    :param method: Correlation method (default pearson correlation)
    :param dropna: Drop nans before calculating correlations
    :return: Correlation matirx as a pandas DataFrame
    """
    if dropna:
        df = df.na.drop()

    col_names = df.columns
    features = df.rdd.map(lambda row: row[0:])
    
    corr_mat = Statistics.corr(features, method=method)
    corr_df = pd.DataFrame(corr_mat)
    
    corr_df.index, corr_df.columns = col_names, col_names
    
    return corr_df
	
