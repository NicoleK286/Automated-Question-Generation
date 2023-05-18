#Importing required libraries and functions
from email import header
import sys
import os
import datetime
import pandas as pd
from cleaning7 import clean # cleaning file
from keywords2 import key   # keyword generation 
from dataprep import convert # datapreparation 
from sher2 import sher        # sherlock code
from sql import sqlquery     #SQL query generation 
from questionssd import ques   # question generation 
from fips import fips        # fips code
import random
from Scraping import scraping
from paraphrasessd2 import *

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords') 
nltk.download('punkt')

#Scraping the data from Indiana-Hub
#link = sys.argv[1] 
#scraping(link)                                              

#Initializing files
filename = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/IndyHub Datasets/File20/data20.csv'
datad = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/IndyHub Datasets/File20/datadescription20.txt'
cold = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/IndyHub Datasets/File20/datacolumn20.csv'

#Initializing files
#filename = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/Main3 Running Examples/Ex17 Mdc/data17.csv'
#datad = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/Main3 Running Examples/Ex17 Mdc/dataDescription17.txt'
#cold = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/Main3 Running Examples/Ex17 Mdc/dataColumn17.csv'


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

cleandf = clean(df,23) # passing the df csv file through cleaning.py 
    #print(cleandf) # print the cleaned data.csv file
    
keyw = key(datad) # pass the data description file in the keywords function 
    #if len(keyw) < 3:
    #   entity = keyw
    #else:
    #   entity = random.sample(keyw,3)

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

#columnd['Description1'] = columnd['Description'].str.split('.').str[0]
columnd['Description1'] = columnd['Description'].astype(str).str.split('.').str[0]

    #columnd_sub = columnd.iloc[:, [0, 2]]

sqlcheat = pd.read_csv('sqlcheatsheet4.csv')

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

print("Corrected Column Order:",newcolcheck)
print("Keywords:", entity)

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
print("Predicted metacategories:",sher_pred)


inp = int(input("Enter Choice: "))
if inp == 1:
        
    g = 'y'
    while g == 'y':
        counter = 0
        for f in range(0,20):
                
                
            sql = sqlquery(cleandf,sher_pred,sqlcheat)
            
            #print(maxind)
            #print(sql)
      
            if counter <2:
                if ((sql[1] == colcheck[maxind] or sql[5] == colcheck[maxind]) and (sql[6] == 'Minimum' or sql[6] == 'Maximum' or sql[6] == 'Average ' or sql[6] == 'sum of')):
                    qs = ques(sql,columnd,cleandf,sher_pred)
                    #stqs = str(qs)
                    #print("The qs generated is:", stqs)
                    #para = get_response(stqs, 1)
                    #print("The paraphrased qs is :", para)
                    counter += 1
                else:
                    counter += 1 
            else:
                if (sql[6] == 'Minimum' or sql[6] == 'Maximum' or sql[6] == 'Average ' or sql[6] == 'sum of'):
                    qs = ques(sql,columnd,cleandf,sher_pred)
                    #stqs = str(qs)
                    #print("The qs generated is:", stqs)
                    #para = get_response(stqs, 1)
                    #print("The paraphrased qs is :", para)
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





































