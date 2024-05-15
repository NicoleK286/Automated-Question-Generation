import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime

#path = 'Dataset6FIPS.csv'
fips_df = pd.read_csv('county2.csv')
fips_list = fips_df['GEO_ID'].tolist()

def get_data_types_df(df):
    # Detect column data types
    data_types = {}
    for col in df.columns:
        numeric_count = 0
        alpha_count = 0
        date_count = 0
        address = 0
        year_count = 0  # New counter for year data
        total_count = 0  # New counter for total values
        for value in df[col]:
            if pd.isna(value):
                continue
            if not isinstance(value, str):
                value = str(value)
            try:
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
                elif value.strip().isdigit() and len(value.strip()) == 4:  # Check for year data
                    year = int(value.strip())
                    if 1900 <= year <= 2100:
                        year_count += 1
                else:
                    float(value)
                    numeric_count += 1
            except ValueError:
                alpha_count += 1
            total_count += 1

        if year_count / total_count > 0.95:  # If more than 95% of values match year data, classify as year
            data_types[col] = 'year'
        elif date_count > 0:
            data_types[col] = 'birth Date'
        elif numeric_count > alpha_count:
            data_types[col] = 'numeric'
            fips_count = sum(df[col].apply(lambda x: x in fips_list if pd.notnull(x) else False))
            fips_percentage = fips_count / len(df[col])
            if fips_percentage > 0.95:
                data_types[col] = 'address'
        else:
            data_types[col] = 'object'

    data_types_df = pd.DataFrame(data_types.items(), columns=['Column', 'Data_Type'])

    return data_types_df

def clean(df, seed):
    # Read the data from file
    #df = pd.read_csv(path)
    #print(df.head())

    data_types_df = get_data_types_df(df)
    print(data_types_df)


    # Split the columns based on datatype
    numeric_cols = [col for col in data_types_df['Column'] if data_types_df.loc[data_types_df['Column'] == col, 'Data_Type'].values[0] == 'numeric']
    object_cols = [col for col in data_types_df['Column'] if data_types_df.loc[data_types_df['Column'] == col, 'Data_Type'].values[0] == 'object']
    date_cols = [col for col in data_types_df['Column'] if data_types_df.loc[data_types_df['Column'] == col, 'Data_Type'].values[0] == 'birth Date']
    year_cols = [col for col in data_types_df['Column'] if data_types_df.loc[data_types_df['Column'] == col, 'Data_Type'].values[0] == 'year']
    address_cols = [col for col in data_types_df['Column'] if data_types_df.loc[data_types_df['Column'] == col, 'Data_Type'].values[0] == 'address']

    # Load the data into separate DataFrames
    df_numeric = df[numeric_cols]
    df_object = df[object_cols]
    df_date = df[date_cols]
    df_year = df[year_cols]
    df_address = df[address_cols]

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
            df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%d %b %Y')
        except ValueError:
            try:
                # Check if date is in the format of "2020-02-26"
                date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%Y-%m-%d')
                df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%d %b %Y')
            except ValueError:
                try:
                    # Check if date is in the format of "2021.03.29 09:03:20.985000000"
                    date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%Y.%m.%d %H:%M:%S.%f')
                    df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%d %b %Y')
                except ValueError:
                    try:
                        # Check if date is in the format of "2021.03.28 22:00:05"
                        date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%Y.%m.%d %H:%M:%S')
                        df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%d %b %Y')
                    except ValueError:
                        try:
                            # Check if date is in the format of "6/30/2019 0:00"
                            date_obj = datetime.strptime(str(df_date[col].iloc[0]), '%m/%d/%Y %H:%M')
                            df_date.loc[:, col] = pd.to_datetime(df_date[col]).dt.strftime('%d %b %Y')
                        except ValueError:
                            # If none of the formats match, assign NaN value
                            df_date.loc[:, col] = df_date[col]

    print("Number of rows before dropping null values:", len(df))
    # Concatenate the numeric, object and datetime DataFrames
    df = pd.concat([df_numeric, df_object, df_date, df_address, df_year], axis=1)

    print("Number of rows before dropping null values:", len(df))

    # Drop duplicate rows and columns
    df = df.drop_duplicates()
    df = df.loc[:, ~df.columns.duplicated()]

    # Drop rows with null values
    print("Number of rows before dropping null values:", len(df))
    df = df.dropna()
    print("Number of rows after dropping null values:", len(df))

    for col in df:
        if col == '_id':
            df = df.drop(columns=['_id'])

    #df = df.sample(frac=1, random_state=seed)

    #print(df.head())
    return df

#clean(path, 23)
