#Importing required libraries and functions
import warnings
warnings.filterwarnings("ignore", message="Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found")
warnings.filterwarnings("ignore", message="Ignore above cudart dlerror if you do not have a GPU set up on your machine")
from email import header
import pyreadstat
import sys
import os
import datetime
import pandas as pd
from cleaning12 import clean_column_names
from cleaning12 import get_data_types_df # get data types
from cleaning12 import clean # cleaning file
from keywords2 import key   # keyword generation 
from dataprep2 import convert # datapreparation 
from sher2 import sher        # sherlock code
from sql3 import sqlquery     #SQL query generation 
from questn12 import ques   # question generation 
from sql_3v import sqlqueryv3     #SQL query generation 
from questn_3v import quesv3   # question generation 
import random
from para7 import *

import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords') 
#nltk.download('punkt')

warnings.filterwarnings("ignore", message="Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found")
warnings.filterwarnings("ignore", message="Ignore above cudart dlerror if you do not have a GPU set up on your machine")
warnings.filterwarnings("ignore", category=UserWarning, message="Evaluating Token.similarity based on empty vectors")
                             
# Common path
# Windows
program_path = 'C:/Users/Nicole/'
#program_path = 'E:/Users/Nicole/'
# Quartz
#program_path = '/N/u/nickoshy/Quartz/'

# Initializing files
#filename = f'{program_path}sherlock-project-master/QGD/testing/Ex4/funds.csv'
#datad = f'{program_path}sherlock-project-master/QGD/testing/Ex4/fundstxt.txt'
#cold = f'{program_path}sherlock-project-master/QGD/testing/Ex4/fundscol.csv'   


# Initializing files
#filename = f'{program_path}sherlock-project-master/QGD/Main3 Running Examples/Ex8/data8.csv'
#datad = f'{program_path}sherlock-project-master/QGD/Main3 Running Examples/Ex8/dataDescription8.txt'
#cold = f'{program_path}sherlock-project-master/QGD/Main3 Running Examples/Ex8/dataColumn8.csv'


#Initializing files
filename = f'{program_path}sherlock-project-master/QGD/IndyHub Datasets/File2/data2.csv'
datad = f'{program_path}sherlock-project-master/QGD/IndyHub Datasets/File2/datadescription2.txt'
cold = f'{program_path}sherlock-project-master/QGD/IndyHub Datasets/File2/datacolumn2.csv'

# Extracting the folder name "Dataset Folder Name"
folder_name = os.path.basename(os.path.dirname(filename))

def read_file(file_path):
    file_extension = file_path.split('.')[-1]
    if file_extension == 'csv':
        df = pd.read_csv(file_path)
    elif file_extension == 'xlsx' or file_extension == 'xls':
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file_extension == 'dat':
        df = pd.read_csv(file_path, delimiter='\t')
    elif file_extension == 'xpt':
        df, metadata = pyreadstat.read_xport(file_path)
    else:
        print('Wrong file type')
        return None
    return df

df = read_file(filename)
columnd = read_file(cold)


orig = df.head()

#date_df = pd.read_csv('date_formats.csv')

# Clean column names
df = clean_column_names(df)

# Get datatypes
datatypes = get_data_types_df(df)

rnd = random.randint(1,100)

#Clean non-numeric data and convert datetime data
cleandf = clean(df, rnd) #
        
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

#collist = list(cleandf.columns)
 
num = columnd.columns.tolist()
if len(num) == 2:
    columnd.columns = ['Column','Description']
else:
    columnd.columns = ['ID','Column','Description']

columnd['Column'] = columnd['Column'].str.replace('_', ' ')
#columnd['Column'] = np.where(columnd['Column'].isin(collist), columnd['Column'], collist[0])
columnd['Description1'] = columnd['Description'].astype(str).str.split('.').str[0]

sqlcheat = pd.read_csv('sqlcheatsheet5.csv')

os.system('cls' if os.name == 'nt' else 'clear')
print("########################################")
# print(entity)

# df.to_csv("output.txt", index=False)
print(filename)
print(datetime.datetime.now())
time = datetime.datetime.now()
#print("Original DF")
#print(orig)
print(columnd)
datatypes['Column'] = datatypes['Column'].str.replace('_', ' ')
DT = datatypes
print(datatypes)
print("")
print("Dataset")
print(cleandf.head())
print("")
warnings.filterwarnings("ignore", category=UserWarning, message="Evaluating Token.similarity based on empty vectors")
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
print("")

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
#print("Highest similarity index:",maxind)
#print("Corrected Column Order:",newcolcheck)
#print("Original Predicted metacategories:",sher_pred)

# Combine newcolcheck and sher_pred into a DataFrame
combined_df = pd.DataFrame({'Column': newcolcheck, 'Predicted metacategories': sher_pred})
#print("Original Combined DF")
#print(combined_df)

# Filter 'Data_Type' values for 'address' and 'year' in datatypes DataFrame
filtered_columns = datatypes[datatypes['Data_Type'].isin(['address', 'birth Date', 'year','county'])]['Column']

meta_category_lists = {
    "date": ["birth Date", "day"],
    "loc": ["address", "area", "birth place", "city", "continent", "country", "location", "region", "county"],
    "prf": ["artist", "creator","director","jockey", "operator", "owner", "person", "education", "industry", "publisher", "service", "manufacturer"],
    "cat": ["affiliate", "affiliation", "album", "brand", "capacity", "category", "classification", "club", "code", "command", "collection",
                "company", "component", "currency", "credit", "description", "family", "format", "gender", "genre", "isbn", "language", "name", "nationality",
                "notes", "order", "organisation", "origin", "plays", "product", "range", "requirement", "religion", "result", "sex", "species",
                "state", "status", "team", "team Name", "type"],
    "num": ["age","class", "depth", "duration", "elevation", "file Size", "grades", "position", "rank", "sales", "symbol", "weight", "ranking"],
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
    
#print("Final Combined DF")

# Rename the 'Predicted metacategories' column to 'Final MetaCategory'
combined_df = combined_df.rename(columns={'Predicted metacategories': 'Final MetaCategory'})

#print(combined_df)


# Final Combined DF modifications
# Merge DataFrames based on the 'Column' column
combined_df = combined_df.merge(datatypes[['Column', 'Data_Type']], on='Column', how='left', suffixes=('', '_y'))
#combined_df = combined_df.merge(combined_df[['Column', 'Final MetaCategory']], on='Column', how='left', suffixes=('', '_y'))
combined_df['Data Examples'] = cleandf.head(1).values.tolist()[0]
combined_df = pd.merge(combined_df, columnd[['Column', 'Description']], on='Column', how='left', suffixes=('', '_y'))
combined_df = combined_df.merge(pd.DataFrame({'Column': combined_df['Column'], 'Spacy Similarity Index': simind}), on='Column', how='left', suffixes=('', '_y'))

# Remove the redundant columns from the merge operation
combined_df = combined_df.drop_duplicates(subset='Column')

combined_df['Original Meta Categories'] = sher_pred

#print(combined_df)

# Handle specific conditions for certain datatypes
for index, row in combined_df.iterrows():
    if row['Original Meta Categories'] == 'year':
        if row['Data_Type'] == 'numeric':
            combined_df.at[index, 'Final MetaCategory'] = 'rank'
            combined_df.at[index, 'Meta Category List'] = 'num'
        elif row['Data_Type'] == 'object':
            combined_df.at[index, 'Final MetaCategory'] = 'code'
            combined_df.at[index, 'Meta Category List'] = 'cat'
    elif row['Original Meta Categories'] == 'county':
        if row['Data_Type'] == 'numeric':
            combined_df.at[index, 'Final MetaCategory'] = 'rank'
            combined_df.at[index, 'Meta Category List'] = 'num'
    elif row['Final MetaCategory'] in meta_category_lists['num']:  # Check if in the "num" list
        if row['Data_Type'] == 'object':
            combined_df.at[index, 'Final MetaCategory'] = 'code'
            combined_df.at[index, 'Meta Category List'] = 'cat'


# Print the final modified table
print("Datatype Characteristics:")
print(combined_df)
print("")
# Extract all values from 'Predicted metacategories' column
sher_pred = combined_df['Final MetaCategory'].tolist()
print("Final Predicted metacategories:", sher_pred)
print("")

# Output dictionary for the initial section
output_data_initial = {
    'Dataset': [folder_name]* len(combined_df),
    'File path': [filename]* len(combined_df),
    'Timestamp': [datetime.datetime.now()]* len(combined_df),
    'Column name': combined_df['Column'],
    'Column Description': combined_df['Description'],
    'Datatype': combined_df['Data_Type'],
    'Data Examples': combined_df['Data Examples'],
    'Original Metacategory': combined_df['Original Meta Categories'],
    'Final Metacategory': combined_df['Final MetaCategory'],
    'Spacy Similarity Index': combined_df['Spacy Similarity Index'],
    'Category group': combined_df['Meta Category List']
}

# Convert the initial output dictionary to a DataFrame
output_df_initial = pd.DataFrame(output_data_initial)


# Save the initial DataFrame to an Excel file with folder name included
output_filename_initial = f"{program_path}sherlock-project-master/QGD/IndyHub Datasets/Main 11 Program Output/{folder_name}_datatype_analysis_m3v.xlsx"
output_df_initial.to_excel(output_filename_initial, index=False)

print("Question Generating dataset")
print("1. Generate Questions")
print("2. Read Data Description")
print("3. Check data keywords")
print("")
            
inp = int(input("Enter Choice: "))
if inp == 1:
    g = 'y'
    output_data2 = [] 
    question_count = 0
    while g == 'y' and question_count < 20:
        counter = 0
        while counter in range(0, 5):
            if question_count < 20:
                sql = sqlqueryv3(cleandf, sher_pred, sqlcheat)
                # Additional code to store data in the list
                q1, que, para, que2, para2, best_version = "", "", "", "", "", ""  # Initialize the variables
                                
                if (sql[1] == colcheck[maxind] or sql[5] == colcheck[maxind] or sql[9] == colcheck[maxind]):
                    qs = quesv3(sql, columnd, cleandf, sher_pred)
                    counter += 1
                else:
                    qs = quesv3(sql, columnd, cleandf, sher_pred)
                    counter += 1
                # Additional code to store data in the list
                output_data2.append({
                    'Dataset': folder_name,
                    'File path': filename,
                    'Timestamp': time,
                    'Keywords': entity,
                    '1st column': sql[1],
                    'Col1 Datatype': DT.loc[DT['Column'] == sql[1], 'Data_Type'].values[0],
                    'Meta Col1': combined_df.loc[combined_df['Column'] == sql[1], 'Final MetaCategory'].values[0],
                    'Col1 cat': combined_df.loc[combined_df['Column'] == sql[1], 'Meta Category List'].values[0],

                    '2nd column': sql[5],
                    'Col2 Datatype': DT.loc[DT['Column'] == sql[5], 'Data_Type'].values[0],
                    'Meta Col2': combined_df.loc[combined_df['Column'] == sql[5], 'Final MetaCategory'].values[0],
                    'Col2 cat': combined_df.loc[combined_df['Column'] == sql[5], 'Meta Category List'].values[0],                                                          
                    'Col2 Operator': sql[6],

                    '3rd column': sql[9],
                    'Col3 Datatype': DT.loc[DT['Column'] == sql[9], 'Data_Type'].values[0],
                    'Meta Col3': combined_df.loc[combined_df['Column'] == sql[9], 'Final MetaCategory'].values[0],
                    'Col3 cat': combined_df.loc[combined_df['Column'] == sql[9], 'Meta Category List'].values[0],                                                          
                    'Col3 Operator': sql[10],

                    'SQL String': str(sql),
                    'Template': qs[0],
                    'Original Question': qs[1],
                    'Best_Version': qs[5],                
                    'Paraphrased Question': qs[2],
                    'Original ColPP Question': qs[3],
                    'Column Paraphrased Question': qs[4]

                })
                question_count += 1
                           
            else:
                break

        g = input("Generate another set of questions(y/n): ")
        os.system('cls' if os.name == 'nt' else 'clear')
    if g == 'n':
        print("Thank You!")
    # Convert the list of dictionaries to a DataFrame
    output_df2 = pd.DataFrame(output_data2)
    
    #Drop duplicates
    #output_df = output_df.drop_duplicates()

    # Save the initial DataFrame to an Excel file with folder name included
    output_filename_initial2 = f"{program_path}sherlock-project-master/QGD/IndyHub Datasets/Main 11 Program Output/{folder_name}_questions_m3v.xlsx"
    output_df2.to_excel(output_filename_initial2, index=False)
    
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





