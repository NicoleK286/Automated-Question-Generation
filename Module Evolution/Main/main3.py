#Importing required libraries and functions
from email import header
import sys
import os
import pandas as pd
from cleaning2 import clean # cleaning file
from keywords2 import key   # keyword generation 
from dataprep import convert # dataprepartion 
from sher2 import sher        # sherlock code
from sql import sqlquery     #SQL query generation 
from questions2 import ques   # question generation 
from fips import fips        # fips code
import random
from Scraping import scraping

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords') 
nltk.download('punkt')

#Scraping the data from Indiana-Hub
#link = sys.argv[1] 
#scraping(link)

#Initializing files
filename = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/datafips1.csv'
datad = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/dataDescriptionfips1.txt'
cold = '/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/dataColumnfips1.csv'
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

orig = df.head()
#Checking for fips dataset
#x = fips(df,cold)
x = 0 #- zip code ; 
#x = 1 
#Only if dataset does not contain fips code
if x == 0:
    columnd = pd.read_csv(cold)   #Reading the column description file
    #filee = []
    #with open(datad,'r') as f:    #Reading the data description file
    #    for line in f:
    #        filee.append(line)
    #print("Data Des:",filee)
    #for i in range(0,len(columnd)):
        #temp = list(columnd.iloc[i,1]) # column description is 2nd column in the file, so we are taking only that
    # print(temp[0])
        #filee = filee + temp # concatenating only column descripton (column 2) + data descritpion
        #print(temp[0])

    #with open('/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/dataDescription10.txt', 'r+') as f:
        #for line in filee:
            #f.writelines(line) # overwrites the data description txt with column descrp+ data des
    #with open(datad,'r') as f2:
    #   a = f2.read()
    #print(datad)  #Prints Data description File
    #print(a)

    #print(columnd.iloc[:,2])
    cleandf = clean(df,0) # passing the df csv file through cleaning.py 
    #print(cleandf) # print the cleaned data.csv file
    
    keyw = key(datad) # pass the data description file in the keywords function 
    #if len(keyw) < 3:
    #   entity = keyw
    #else:
    #   entity = random.sample(keyw,3)

    print(keyw)
    
    entity = keyw 
    #print(entity) # prints the keywords 

    convert(cleandf) # pass the cleaned data.csv through convert function to transpose the values
    ready = pd.read_csv("test.csv")
    #print(ready)



    del ready['Unnamed: 0']
    sher_pred = sher(ready)
    print(sher_pred)

 
    num = columnd.columns.tolist()
    if len(num) == 2:
        columnd.columns = ['Column','Description']
    else:
        columnd.columns = ['ID','Column','Description']

    columnd['Description1'] = columnd['Description'].str.split('.').str[0]
    columnd_sub = columnd.iloc[:, [0, 2]]

    sqlcheat = pd.read_csv('sqlcheatsheet4.csv')

    os.system('cls' if os.name == 'nt' else 'clear')
    print("########################################")
    #print(entity)
    print("Question Generating dataset")
    print("1. Generate Questions")
    print("2. Read Data Description")
    print("3. Check data keywords")
    print(filename)
    print ("Original DF")
    print (orig)
    print(columnd_sub)
    print ("Cleaned Random DF")
    print(cleandf.head())
    simind = []
    import spacy
    nlp = spacy.load('en_core_web_lg')
    colcheck = list(cleandf.columns)
    #print ("colcheck", colcheck)
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




