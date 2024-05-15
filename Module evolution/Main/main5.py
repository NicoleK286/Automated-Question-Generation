import sys
import os
import datetime
import pandas as pd
from cleaning10 import get_data_types_df
from cleaning10 import clean
from keywords2 import key
from dataprep import convert
from sher2 import sher
from sql2 import sqlquery
from questn import ques
import random
from para2 import *
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

output_file = "output.txt"
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
cleandf = clean(df, 47)
keyw = key(datad)
entity = keyw
convert(cleandf)
ready = pd.read_csv("test.csv")
del ready['Unnamed: 0']
sher_pred = sher(ready)
num = columnd.columns.tolist()
if len(num) == 2:
    columnd.columns = ['Column', 'Description']
else:
    columnd.columns = ['ID', 'Column', 'Description']
columnd['Description1'] = columnd['Description'].astype(str).str.split('.').str[0]
sqlcheat = pd.read_csv('sqlcheatsheet4.csv')

with open(output_file, "a") as f:
    f.write("########################################\n")
    f.write("Question Generating dataset\n")
    f.write("1. Generate Questions\n")
    f.write("2. Read Data Description\n")
    f.write("3. Check data keywords\n")
    f.write(filename + "\n")
    f.write(str(datetime.datetime.now()) + "\n")
    f.write("Original DF\n")
    f.write(str(orig) + "\n")
    f.write(str(columnd) + "\n")
    f.write(str(datatypes) + "\n")
    f.write("Cleaned Random DF\n")
    f.write(str(cleandf.head()) + "\n")
    f.write("Keywords: " + str(entity) + "\n")
    
    simind = []
    import spacy
    nlp = spacy.load('en_core_web_lg')
    colcheck = cleandf.columns.tolist()
    newcolcheck = [w for w in colcheck if w.lower() not in stopwords.words('english')]
    
    for i in newcolcheck:
        sum = 0
        for j in entity:
            x = nlp(i)
            y = nlp(j)
            if len(x) > 0 and len(y) > 0:
                z = x[0].similarity(y[0])
                sum += z
        simind.append(sum)
    
    maxv = max(simind)
    maxind = simind.index(maxv)
    f.write("Highest similarity index: " + str(maxind) + "\n")
    f.write("Original Predicted metacategories: " + str(sher_pred) + "\n")
    
    combined_df = pd.DataFrame({'Column': newcolcheck, 'Predicted metacategories': sher_pred})
    f.write("Original Combined DF\n")
    f.write(str(combined_df) + "\n")
    
    filtered_columns = datatypes[datatypes['Data_Type'].isin(['address', 'year'])]['Column']
    
    for column in filtered_columns:
        combined_df.loc[combined_df['Column'] == column, 'Predicted metacategories'] = datatypes.loc[
            datatypes['Column'] == column, 'Data_Type'].values[0]
    
    f.write("Final Combined DF\n")
    f.write(str(combined_df) + "\n")
    
    sher_pred = combined_df['Predicted metacategories'].tolist()
    f.write("Final Predicted metacategories: " + str(sher_pred) + "\n")
    
    inp = int(input("Enter Choice: "))
    if inp == 1:
        g = 'y'
        while g == 'y':
            counter = 0
            for f in range(0, 20):
                sql = sqlquery(cleandf, sher_pred, sqlcheat)

                if counter < 2:
                    if (
                            (sql[1] == colcheck[maxind] or sql[5] == colcheck[maxind]) and (
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

        if g == 'n':
            f.write("Thank You!\n")

    elif inp == 2:
        with open(datad, 'r') as f2:
            file_contents = f2.read()
            f.write(file_contents + "\n")

    elif inp == 3:
        if len(keyw) >= 3:
            f.write("Enter the number of words in theme <= " + str(len(keyw)) + "\n")
            sel = int(input(""))
            if sel <= len(keyw):
                f.write(str(random.sample(keyw, sel)) + "\n")
            else:
                f.write("Wrong Entry\n")
        else:
            f.write(str(keyw) + "\n")

    else:
        f.write("Wrong Entry\n")
