def clean(df):
    df.rename(columns = {'DATE': 'date'}, inplace = True)
    col = list(df.columns)
    #Check for gargabe string in numerical column
    import numpy as np
    import pandas as pd
    
    for i in range(0,len(col)):
       df = df[np.isfinite(pd.to_numeric(df[col[i]], errors="coerce"))]
    
    
    #Checking and Dropping null values
    if df.isnull().values.any() == 'True':
        df = df.dropna()
   
    #Dropping duplicate columns
    df.drop_duplicates()
    
    #Checking for stop words in columns
    col = list(df.columns)
    import nltk
    nltk.download('stopwords')          #Scope: Removal of stopwords from column description file
    from nltk.corpus import stopwords
    filtered_words = [word for word in col if word not in stopwords.words('english')]
    df.columns = filtered_words
    print(col)

    if '_id' in col:
        df = df.drop(columns = ['_id'])
    
    if 'date' in col:
        df['date'] = df['date'].str[:10]
    
    if 'date' in col:
        for i in range(0,len(df['date'])):
            year = df['date'].iloc[i][:4]
            month = df['date'].iloc[i][5:7]
            day = df['date'].iloc[i][8:10]
            if month == '01':
                month = 'Jan'
            elif month == '02':
                month = 'Feb'
            elif month == '03':
                month = 'Mar'
            elif month == '04':
                month = 'Apr'
            elif month == '05':
                month = 'May'
            elif month == '06':
                month = 'Jun'
            elif month == '07':
                month = 'Jul'
            elif month == '08':
                month = 'Aug'
            elif month == '09':
                month = 'Sep'
            elif month == '10':
                month = 'Oct'
            elif month == '11':
                month = 'Nov'
            elif month == '12':
                month = 'Dec'
            
            d = month + ' ' + day + ', '  + year
            df['date'].iloc[i] = d

        col1 = list(df.columns)
        print (col1)

#We have a scope of optimization here: Instead use the round() function

        temp = 0
        for x in col1:
            y = df[x].dtypes
            if y == 'float64':
                sav = x
                temp += 1
        if temp > 0:
            counter = -1                
            for i in df[sav]:
                counter += 1
                i = str(round(i,2))
                df[sav].iloc[counter] = i
        
    print(df.head())
    
    return df
