import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords

def clean(df, seed):
    # Read the data from file
    #df = pd.read_csv(file_path)
    
    # Detect column data types
    data_types = {}
    for col in df.columns:
        numeric_count = 0
        alpha_count = 0
        for value in df[col]:
            if pd.isna(value):
                continue
            if not isinstance(value, str):
                value = str(value)
            try:
                # check if the value contains any operators
                if any(op in value for op in ['=', '>', '<', '<=', '>=']):
                    numeric_count += 1
                else:
                    float(value)
                    numeric_count += 1
            except ValueError:
                alpha_count += 1
        if numeric_count > alpha_count:
            data_types[col] = 'numeric'
        else:
            data_types[col] = 'object'

    # Split the columns based on datatype
    numeric_cols = [col for col in data_types.keys() if data_types[col] == 'numeric']
    object_cols = [col for col in data_types.keys() if data_types[col] == 'object']

    # Load the data into separate DataFrames
    df_numeric = df[numeric_cols]
    df_object = df[object_cols]

    # Drop rows with non-numeric values for numeric columns
    for col in numeric_cols:
        # check if the column contains operators
        has_operators = any(op in col for op in ['=', '>', '<', '<=', '>='])
        if has_operators:
            df_numeric = df_numeric[df_numeric[col].apply(lambda x: any(op in str(x) for op in ['=', '>', '<', '<=', '>=']) or pd.to_numeric(x, errors='coerce').notnull())]
        else:
            df_numeric = df_numeric[pd.to_numeric(df_numeric[col], errors='coerce').notnull()]

    # Concatenate the numeric and object DataFrames
    df = pd.concat([df_numeric, df_object], axis=1)



    # Drop duplicate rows and columns
    df = df.drop_duplicates()
    df = df.loc[:, ~df.columns.duplicated()]

    # Drop rows with null values
    df = df.dropna()
    
    for col in df:
	    if col =='_id':
		    df = df.drop(columns = ['_id'])

    df = df.sample(frac=1, random_state=seed)

    return df
