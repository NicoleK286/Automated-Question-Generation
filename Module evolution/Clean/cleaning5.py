import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime
#path = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/IndyHub Datasets/File3/data3.csv'
#seed = 23

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

    # Remove everything after "T" in datetime columns
    for col in date_cols:
        #df_date[col] = df_date[col].str.replace('T', '')
        df_date[col] = df_date[col].apply(lambda x: x.split('T')[0])
        df_date[col] = pd.to_datetime(df_date[col])
        df_date[col] = df_date[col].dt.strftime('%d %b %Y')    

        
    # Concatenate the numeric, object and datetime DataFrames
    df = pd.concat([df_numeric, df_object, df_date], axis=1)

    # Check for stop words in column names
    #nltk.download('stopwords')          #Scope: Removal of stopwords from column description file    
    #df.columns = [word for word in df.columns if word not in stopwords.words('english')]
    #print (df.columns)

    # Drop duplicate rows and columns
    df = df.drop_duplicates()
    df = df.loc[:, ~df.columns.duplicated()]

    # Drop rows with null values
    df = df.dropna()
    
    for col in df:
	    if col =='_id':
		    df = df.drop(columns = ['_id'])

    #df = df.sample(frac=1, random_state=seed)
    

    #print (df.head())
    return df

#clean(path, seed)




