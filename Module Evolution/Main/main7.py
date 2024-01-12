#Importing required libraries and functions
from email import header
import sys
import os
import datetime
import warnings
import pandas as pd
from cleaning12 import clean_column_names
from cleaning12 import get_data_types_df # get data types
from cleaning12 import clean # cleaning file
from keywords2 import key   # keyword generation 
from dataprep import convert # datapreparation 
from sher2 import sher        # sherlock code
from sql4 import sqlquery     #SQL query generation 
from questn5 import ques   # question generation 
import random
from para2 import *

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords') 
nltk.download('punkt')

warnings.filterwarnings("ignore", category=UserWarning, message="Evaluating Token.similarity based on empty vectors")
                                       

# Initializing files
#filename = 'C:/Users/Nicole/sherlock-project-master/QGD/testing/Ex4/funds.csv'
#datad = 'C:/Users/Nicole/sherlock-project-master/QGD/testing/Ex4/fundstxt.txt'
#cold = 'C:/Users/Nicole/sherlock-project-master/QGD/testing/Ex4/fundscol.csv'   

# Initializing files
filename = 'C:/Users/Nicole/sherlock-project-master/QGD/Main3 Running Examples/Ex11 Mdc/data11.csv'
datad = 'C:/Users/Nicole/sherlock-project-master/QGD/Main3 Running Examples/Ex11 Mdc/dataDescription11.txt'
cold = 'C:/Users/Nicole/sherlock-project-master/QGD/Main3 Running Examples/Ex11 Mdc/dataColumn11.csv'


#Initializing files
#filename = 'C:/Users/Nicole/sherlock-project-master/QGD/IndyHub Datasets/File26/OES_Emp_Wage_IN2022_data.xlsx'
#datad = 'C:/Users/Nicole/sherlock-project-master/QGD/IndyHub Datasets/File26/OES_Emp_Wage_IN2022_dataDescription.txt'
#cold = 'C:/Users/Nicole/sherlock-project-master/QGD/IndyHub Datasets/File26/OES_Emp_Wage_IN2022_dataColumn.xlsx'


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


# Clean column names
df = clean_column_names(df)

# Get datatypes
datatypes = get_data_types_df(df)

#Clean non-numeric data and convert datetime data
cleandf = clean(df,47) #
    
    
keyw = key(datad) # pass the data description file in the keywords function 


#print(keyw)
    
entity = keyw 
    #print(entity) # prints the keywords 

convert(cleandf) # pass the cleaned data.csv through convert function to transpose the values
ready = pd.read_csv("test.csv")
    #print(ready)



del ready['Unnamed: 0']
sher_pred = sher(ready)
#print(sher_pred)


 
num = columnd.columns.tolist()
if len(num) == 2:
    columnd.columns = ['Column','Description']
else:
    columnd.columns = ['ID','Column','Description']

columnd['Column'] = columnd['Column'].str.replace('_', ' ')
columnd['Description1'] = columnd['Description'].astype(str).str.split('.').str[0]


sqlcheat = pd.read_csv('sqlcheatsheet5.csv')

os.system('cls' if os.name == 'nt' else 'clear')
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
    #print(i)
    i = i.replace("_"," ")
    newcolcheck.append(i)

newcolcheck = [word for word in newcolcheck if word.lower() not in stopwords.words('english')]

print("Keywords:", entity)

warnings.filterwarnings("ignore", category=UserWarning, message="Evaluating Token.similarity based on empty vectors")

for i in newcolcheck:
    sum = 0
    for j in entity:
        x = nlp(i)
        y = nlp(j)
        z = x[0].similarity(y[0])
        sum += z
    simind.append(sum)
    #print(simind)

maxv = max(simind)
maxind = simind.index(maxv)
print("Highest similarity index:",maxind)
#print("Corrected Column Order:",newcolcheck)
print("Original Predicted metacategories:",sher_pred)

# Combine newcolcheck and sher_pred into a DataFrame
combined_df = pd.DataFrame({'Column': newcolcheck, 'Predicted metacategories': sher_pred})
print("Original Combined DF")
print(combined_df)

# Filter 'Data_Type' values for 'address' and 'year' in datatypes DataFrame
filtered_columns = datatypes[datatypes['Data_Type'].isin(['address', 'birth Date', 'year'])]['Column']

meta_category_lists = {
    "date": ["birth Date", "day"],
    "loc": ["address", "area", "birth place", "city", "continent", "country", "location", "region", "county"],
    "prf": ["artist", "creator","director","jockey", "operator", "owner", "person", "education", "industry", "publisher", "service", "manufacturer"],
    "cat": ["affiliate", "affiliation", "album", "brand", "capacity", "category", "classification", "class", "club", "code", "command", "collection",
            "company", "component", "currency", "credit", "description", "family", "format", "gender", "genre", "iSBN", "language", "name", "nationality",
            "notes", "order", "organisation", "origin", "plays", "position", "product", "range", "requirement", "religion", "result", "sex", "species",
            "state", "status", "team", "team Name", "type"],
    "num": ["age", "depth", "duration", "elevation", "file Size", "grades", "rank", "sales", "symbol", "weight", "ranking"],
    "year": ["year"]
}

# Iterate over the filtered_columns
for column in filtered_columns:
    # Find the matching row in combined_df and update 'Predicted metacategories'
    combined_df.loc[combined_df['Column'] == column, 'Predicted metacategories'] = datatypes.loc[datatypes['Column'] == column, 'Data_Type'].values[0]

# Create a new column 'Meta Category List'
combined_df['Meta Category List'] = None  # Initialize the column with None

# Iterate through the dictionary and assign the list label to the corresponding meta categories
for list_label, meta_categories in meta_category_lists.items():
    combined_df.loc[combined_df['Predicted metacategories'].isin(meta_categories), 'Meta Category List'] = list_label

print("Final Combined DF")
print(combined_df)

# Extract all values from 'Predicted metacategories' column
sher_pred = combined_df['Predicted metacategories'].tolist()
#print("Final Predicted metacategories:", sher_pred)


            
inp = int(input("Enter Choice: "))
if inp == 1:
        
    g = 'y'
    while g == 'y':
        counter = 0
        for f in range(0,20):

            sql = sqlquery(cleandf,sher_pred,sqlcheat)
      
            if counter <5:
                if ((sql[1] == colcheck[maxind] or sql[5] == colcheck[maxind]) and (sql[6] == "Minimum" or sql[6] == "Maximum" or sql[6] == "Average " or sql[6] == "COUNT" or sql[6] == "Sum of" or sql[6] == "Equal to" or sql[6] == "Not Equal to" or sql[6] == "Lesser than" or sql[6] == "Greater than")):
                    qs = ques(sql,columnd,cleandf,sher_pred)
                    counter += 1
                else:
                    counter += 1 
            else:
                if (sql[6] == "Minimum" or sql[6] == "Maximum" or sql[6] == "Average " or sql[6] == "COUNT" or sql[6] == "Sum of" or sql[6] == "Equal to" or sql[6] == "Not Equal to" or sql[6] == "Lesser than" or sql[6] == "Greater than"):
                    qs = ques(sql,columnd,cleandf,sher_pred)
                else:
                    continue


        g = input("Generate another set of questions(y/n): ")
        os.system('cls' if os.name == 'nt' else 'clear')
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





































