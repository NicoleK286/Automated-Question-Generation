def sqlquery(test,sherlock_prediction,sqlcheatsheet):
    import random
    sql = []
    st = ["address","location","county","age","gender","race","collection",'category','result','city','club','year','day']
    x = []
    t = -1
    col = list(test.columns)
    sql.append("SELECT")
    for i in sherlock_prediction:
        t += 1
        if i in st:
            x.append(t)  #COLUMN1
    
    #print(x)
            
    ra = random.choice(x)
    #print(ra)
    sql.append(col[ra])    # INDEX COLUMN1
    sql.append("FROM")
    sql.append("test")
    sql.append("WHERE")
    guess5 = random.randint(0,len(col)-1)
    while guess5 == ra:
        guess5 = random.randint(0,len(col)-1)  #COLUMN2
    sql.append(col[guess5])
    checker = sherlock_prediction[guess5]
    selection = sqlcheatsheet[sqlcheatsheet['Category'] == checker] #ROW WHERE METACATEGORY IS PRESENT
    selection = selection.loc[:, (selection != 0).any(axis=0)]   #REMOVE COLUMNS WHERE = 0
    selection = selection.drop(columns = ['Category']) #DROP CAT COLUMN
    map_col = list(selection.columns)  #OPERATOR COLUMNS = 1 ADDED
        #print(map_col)
    if(len(map_col) == 3):
        guess2 = random.randint(0,len(map_col)-2)   #
    else:
        guess2 = random.randint(2,len(map_col)-1)
    sql.append(map_col[guess2])
    guess3 = random.randint(0,len(test[col[guess5]])-1)
    value = test[col[guess5]].iloc[guess3]
    sql.append(value)
        

   
    
    return sql
