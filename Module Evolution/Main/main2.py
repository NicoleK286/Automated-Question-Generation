#Importing required libraries and functions
import sys
import os
import pandas as pd
from cleaning import clean
from keywords import key
from dataprep import convert
from sher import sher
from sql import sqlquery
from questions import ques
from fips import fips
import random
from Scraping import scraping

# #Scraping the data from Indiana-Hub
#link = sys.argv[1]
#scraping(link)

#Initializing files
filename = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/testing/Ex3/data2.csv'
datad = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/testing/Ex3/dataDescription.txt'
cold = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/testing/Ex3/dataColumn.csv'
filepath, file_extension = os.path.splitext(filename)

#Check the file extension for processing
if(file_extension == ".csv"):
    df = pd.read_csv(filename)
elif(file_extension == ".xlsx"):
    df = pd.read_excel(filepath)
elif(file_extension == ".xls"):
    df = pd.read_excel(filepath)
else:
    print("Wrong file type")

#Checking for fips dataset
#x = fips(df,cold)
x = 0
#Only if dataset does not contain fips code
if x == 0:
    columnd = pd.read_csv(cold)   #Reading the column description file
    filee = []
    with open(datad,'r') as f:    #Reading the data description file
        for line in f:
            filee.append(line)     #Appending the data description file
    print(filee)
    for i in range(0,len(columnd)):
        temp = list(columnd.iloc[i,1])  #Since the column description in the second column we are adding the column number as "2"
    # print(temp[0])filee
        filee = filee + temp #concatenating only column description (column name not included) and data description file

    with open('/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/testing/Ex3/dataDescription.txt', 'r+') as f:
        for line in filee:
            f.writelines(line) #overwrites Filee to combine column des and data des 
    #with open(datad,'r') as f2:
    #   a = f2.read()

    #print(a)
    datad = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/testing/Ex3/dataDescription.txt'
    print(columnd.iloc[:,2])
    cleandf = clean(df) #changed the file name as cleandf
    keyw = key(datad)
    #if len(keyw) < 3:
    #   entity = keyw
    #else:
    #   entity = random.sample(keyw,3)

    entity = keyw
    print(entity)
    convert(cleandf)
    ready = pd.read_csv("test.csv")
    del ready['Unnamed: 0']
    sher_pred = sher(ready)


    num = columnd.columns.tolist()
    if len(num) == 2:
        columnd.columns = ['Column','Description']
    else:
        columnd.columns = ['ID','Column','Description']

    columnd['Description1'] = columnd['Description'].str.split('.').str[0]
    sqlcheat = pd.read_csv('sqlcheatsheet3.csv')

    os.system('cls' if os.name == 'nt' else 'clear')
    print("########################################")
    print(entity)
    print("Question Generating dataset")
    print("1. Generate Questions")
    print("2. Read Data Description")
    print("3. Check data keywords")
    print(columnd)
    print(df.head())
    simind = []
    import spacy
    nlp = spacy.load('en_core_web_lg')
    colcheck = list(cleandf.columns)
    newcolcheck = []
    for i in colcheck:
        #print(i)
        i = i.replace("_"," ")
        newcolcheck.append(i)
    #print(colcheck)
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
    print(maxind)
    print(sher_pred)
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
                    if ((sql[1] == colcheck[maxind] or sql[5] == colcheck[maxind]) and (sql[6] == 'Minimum' or sql[6] == 'Maximum' or sql[6] == 'Average ' or sql[6] == 'COUNT' or sql[6] == 'sum of')):
                        ques(sql,columnd,cleandf,sher_pred)
                        counter += 1
                    else:
                        counter += 1 
                else:
                    if (sql[6] == 'Minimum' or sql[6] == 'Maximum' or sql[6] == 'Average ' or sql[6] == 'COUNT' or sql[6] == 'sum of'):
                        ques(sql,columnd,cleandf,sher_pred)
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
        if len(keyw) >=3:
            print("Enter the number of words in theme <=", len(keyw))
            sel = int(input(""))
            if(sel <= len(keyw)):
                print(random.sample(keyw,sel))
            else:
                print("Wrong Entry")

        else:
            print(keyw)
    else:
        print("Wrong Entry")
            
    
else:
    print("Thank you")









