import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime

def clean(df, seed):
    # Read the data from file
    #df = pd.read_csv(path)
    
    # Detect column data types
    data_types = {}
    for col in df.columns:
        numeric_count = 0
        alpha_count = 0
        date_count = 0
        for value in df[col]:
            if pd.isna(value):
                continue
            if not isinstance(value, str):
                value = str(value)
            try:
                # check if the value contains any operators
                if any(op in value for op in ['=', '>', '<', '<=', '>=']):
                    numeric_count += 1
                elif re.match('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', value):
                    date_count += 1
                elif re.match('\d{4}-\d{2}-\d{2}', value):
                    date_count += 1
                elif re.match('\d{1,2}/\d{1,2}/\d{4}', value):
                    date_count += 1
                elif re.match('\d{4}\.\d{2}\.\d{2}\s\d{2}:\d{2}:\d{2}', value):
                    date_count += 1
                elif re.match('\d{4}\.\d{2}\.\d{2}\s\d{2}:\d{2}:\d{2}\.\d{9}', value):
                    date_count += 1
                else:
                    float(value)
                    numeric_count += 1
            except ValueError:
                alpha_count += 1
        if date_count > 0:
            data_types[col] = 'datetime'
        elif numeric_count > alpha_count:
            data_types[col] = 'numeric'
        else:
            data_types[col] = 'object'

    # Split the columns based on datatype
    numeric_cols = [col for col in data_types.keys() if data_types[col] == 'numeric']
    object_cols = [col for col in data_types.keys() if data_types[col] == 'object']
    date_cols = [col for col in data_types.keys() if data_types[col] == 'datetime']

    # Load the data into separate DataFrames
    df_numeric = df[numeric_cols]
    df_object = df[object_cols]
    df_date = df[date_cols]

    # Drop rows with non-numeric values for numeric columns
    for col in numeric_cols:
        # check if the column contains operators
        has_operators = any(op in col for op in ['=', '>', '<', '<=', '>='])
        if has_operators:
            df_numeric = df_numeric[df_numeric[col].apply(lambda x: any(op in str(x) for op in ['=', '>', '<', '<=', '>=']) or pd.to_numeric(x, errors='coerce').notnull())]
        else:
            df_numeric = df_numeric[pd.to_numeric(df_numeric[col], errors='coerce').notnull()]

    # Remove everything after "T" in datetime columns and convert to desired format
    for col in date_cols:
        df_date.loc[:, col] = df_date[col].apply(lambda x: re.sub('T.*', '', str(x)) if pd.notnull(x) else x)
        try:
            # Check if date is in the format of "5/24/2011"
            date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%m/%d/%Y')
            df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%m-%d-%Y')
        except ValueError:
            try:
                # Check if date is in the format of "2020-02-26"
                date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%Y-%m-%d')
                df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%m-%d-%Y')
            except ValueError:
                try:
                    # Check if date is in the format of "2021.03.29 09:03:20.985000000"
                    date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%Y.%m.%d %H:%M:%S.%f')
                    df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%m-%d-%Y')
                except ValueError:
                    try:
                    # Check if date is in the format of "2021.03.28 22:00:05"
                        date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%Y.%m.%d %H:%M:%S')
                        df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%m-%d-%Y')
                    except ValueError:
                        try:
                            # Check if date is in the format of "6/30/2019 0:00"
                            date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%m/%d/%Y %H:%M')
                            df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%m-%d-%Y')
                        except ValueError:
                            # If none of the formats match, don't change value
                            df_date.loc[:, col] = df_date[col]


                    
     # Concatenate the numeric, object and datetime DataFrames
    df = pd.concat([df_numeric, df_object, df_date], axis=1)

    # Check for stop words in column names
    # nltk.download('stopwords')  # Scope: Removal of stopwords from column description file    
    # df.columns = [word for word in df.columns if word not in stopwords.words('english')]
    # print(df.columns)

    # Drop duplicate rows and columns
    df = df.drop_duplicates()
    df = df.loc[:, ~df.columns.duplicated()]

    # Drop rows with null values
    df = df.dropna()

    for col in df:
        if col == '_id':
            df = df.drop(columns=['_id'])

    df = df.sample(frac=1, random_state=seed)

    # print(df.head())
    return df



