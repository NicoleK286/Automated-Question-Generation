import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime

#path = 'Dataset6FIPS.csv'
fips_df = pd.read_csv('county2.csv')
fips_list = fips_df['GEO_ID'].tolist()
county_list1 = fips_df['NAME_ONLY'].tolist()
county_list2 = fips_df['NAME'].tolist()

# Function to clean column names
def clean_column_names(df):
    # Replace underscores with spaces in column names
    df.columns = df.columns.str.replace('_', ' ')
    return df


def get_data_types_df(df):
    # Detect column data types
    data_types = {}
    for col in df.columns:
        numeric_count = 0
        alpha_count = 0
        date_count = 0
        county_count = 0
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
                elif any(name in value for name in county_list1) or any(name in value for name in county_list2):
                    county_count += 1
                else:
                    float(value) or int(value)
                    numeric_count += 1
            except ValueError:
                alpha_count += 1
            total_count += 1

        if year_count / total_count > 0.95:  # If more than 95% of values match year data, classify as year
            data_types[col] = 'year'
        elif date_count/ total_count  > 0.95:
            data_types[col] = 'birth Date'
        elif county_count / total_count > 0.95:
            data_types[col] = 'county'
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

    print("Total number of rows:", len(df))

    # Drop duplicate rows and columns
    df = df.drop_duplicates()
    df = df.loc[:, ~df.columns.duplicated()]

    # Drop rows with null values
    print("Number of rows before dropping null values:", len(df))
    #df = df.fillna(0)
    print("Number of rows after dropping null values:", len(df))

    columns_to_drop = ['id', '_id', ' id', 'id ']
    for col in df.columns:
        if col.strip().lower() in columns_to_drop:
            df = df.drop(columns=[col])
            

    df = df.sample(frac=1, random_state=seed)

    #print(df.head())
    return df

#clean(path, 23)
