# Importing required libraries and functions
from email import header
import sys

sys.stdout = open("/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/IndyHub Datasets/Clean10 Run1 output/Ex9_c10_m5.txt", "w")

import os
import datetime
import pandas as pd
from cleaning10 import get_data_types_df  # get data types
from cleaning10 import clean  # cleaning file
from keywords2 import key  # keyword generation
from dataprep import convert  # datapreparation
from sher2 import sher  # sherlock code
from sql2 import sqlquery  # SQL query generation
from questn import ques  # question generation
import random
from para2 import *

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


# Initializing files
#filename = 'C:Users/Nicole/sherlock-project-master/QGD/testing/Ex4/funds.csv'
#datad = 'C:Users/Nicole/sherlock-project-master/QGD/testing/Ex4/fundstxt.txt'
#cold = 'C:Users/Nicole/sherlock-project-master/QGD/testing/Ex4/fundscol.csv'   

# Initializing files
#filename = 'C:Users/Nicole/sherlock-project-master/QGD/Main3 Running Examples/Ex9/data9.csv'
#datad = 'C:Users/Nicole/sherlock-project-master/QGD/Main3 Running Examples/Ex9/dataDescription9.txt'
#cold = 'C:Users/Nicole/sherlock-project-master/QGD/Main3 Running Examples/Ex9/dataColumn9.csv'


#Initializing files
filename = 'C:Users/Nicole/sherlock-project-master/QGD/IndyHub Datasets/File2/data2.csv'
datad = 'C:Users/Nicole/sherlock-project-master/QGD/IndyHub Datasets/File2/datadescription2.txt'
cold = 'C:Users/Nicole/sherlock-project-master/QGD/IndyHub Datasets/File2/datacolumn2.csv'


def read_file(file_path):
    file_extension = file_path.split('.')[-1]
    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    elif file_extension == 'xlsx' or file_extension == 'xls':
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        print('Wrong file type')
        return None
    return df


df = read_file(filename)
columnd = read_file(cold)


orig = df.head()

datatypes = get_data_types_df(df)

cleandf = clean(df, 47)  # passing the df csv file through cleaning.py
# print(cleandf) # print the cleaned data.csv file

keyw = key(datad)  # pass the data description file in the keywords function


# print(keyw)

entity = keyw
# print(entity) # prints the keywords

convert(cleandf)  # pass the cleaned data.csv through convert function to transpose the values
ready = pd.read_csv("test.csv")
# print(ready)


del ready['Unnamed: 0']
sher_pred = sher(ready)
# print(sher_pred)


num = columnd.columns.tolist()
if len(num) == 2:
    columnd.columns = ['Column', 'Description']
else:
    columnd.columns = ['ID', 'Column', 'Description']

# columnd['Description1'] = columnd['Description'].str.split('.').str[0]
columnd['Description1'] = columnd['Description'].astype(str).str.split('.').str[0]

# columnd_sub = columnd.iloc[:, [0, 2]]

sqlcheat = pd.read_csv('sqlcheatsheet4.csv')

# os.system('cls' if os.name == 'nt' else 'clear')
print("########################################")
# print(entity)

print("Question Generating dataset")
print("1. Generate Questions")
print("2. Read Data Description")
print("3. Check data keywords")
# df.to_csv("output.txt", index=False)
print(filename)
print(datetime.datetime.now())
print("Original DF")
print(orig)
print(columnd)
datatypes['Column'] = datatypes['Column'].str.replace('_', ' ')
print(datatypes)
print("Cleaned Random DF")
print(cleandf.head())

simind = []

import spacy

nlp = spacy.load('en_core_web_lg')
colcheck = list(cleandf.columns)
# print("colcheck", colcheck)
newcolcheck = []
for i in colcheck:
    # print(i)
    i = i.replace("_", " ")
    newcolcheck.append(i)

newcolcheck = [word for word in newcolcheck if word.lower() not in stopwords.words('english')]

print("Keywords:", entity)

for i in newcolcheck:
    sum = 0
    for j in entity:
        x = nlp(i)
        y = nlp(j)
        z = x[0].similarity(y[0])
        sum += z
    simind.append(sum)
    # print(simind)

maxv = max(simind)
maxind = simind.index(maxv)
print("Highest similarity index:", maxind)
print("Corrected Column Order:",newcolcheck)
print("Original Predicted metacategories:", sher_pred)

# Combine newcolcheck and sher_pred into a DataFrame
combined_df = pd.DataFrame({'Column': newcolcheck, 'Predicted metacategories': sher_pred})
print("Original Combined DF")
print(combined_df)

# Filter 'Data_Type' values for 'address' and 'year' in datatypes DataFrame
filtered_columns = datatypes[datatypes['Data_Type'].isin(['address','birth Date', 'year'])]['Column']

# Iterate over the filtered_columns
for column in filtered_columns:
    # Find the matching row in combined_df and update 'Predicted metacategories'
    combined_df.loc[combined_df['Column'] == column, 'Predicted metacategories'] = datatypes.loc[
        datatypes['Column'] == column, 'Data_Type'].values[0]
print("Final Combined DF")
print(combined_df)

# Extract all values from 'Predicted metacategories' column
sher_pred = combined_df['Predicted metacategories'].tolist()
print("Final Predicted metacategories:", sher_pred)


inp = int(input("Enter Choice: "))
if inp == 1:

    g = 'y'
    while g == 'y':
        counter = 0
        for f in range(0, 20):

            sql = sqlquery(cleandf, sher_pred, sqlcheat)

            # print(maxind)
            # print(sql)

            if counter < 2:
                if ((sql[1] == colcheck[maxind] or sql[5] == colcheck[maxind]) and (
                        sql[6] == 'Minimum' or sql[6] == 'Maximum' or sql[6] == 'Average ' or sql[6] == 'sum of')):
                    qs = ques(sql, columnd, cleandf, sher_pred)
                    counter += 1
                else:
                    counter += 1
            else:
                if (sql[6] == 'Minimum' or sql[6] == 'Maximum' or sql[6] == 'Average ' or sql[6] == 'sum of'):
                    qs = ques(sql, columnd, cleandf, sher_pred)
                else:
                    continue

        g = input("Generate another set of questions(y/n): ")
        # os.system('cls' if os.name == 'nt' else 'clear')
    if g == 'n':
        print("Thank You!")
elif inp == 2:
    f = open(datad, 'r')
    file_contents = f.read()
    print(file_contents)
elif inp == 3:
    import random

    if len(keyw) >= 3:
        print("Enter the number of words in theme <=", len(keyw))
        sel = int(input(""))
        if sel <= len(keyw):
            print(random.sample(keyw, sel))
        else:
            print("Wrong Entry")
    else:
        print(keyw)
else:
    print("Wrong Entry")

sys.stdout.close()
