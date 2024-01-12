def sqlquery(test,sherlock_prediction,sqlcheatsheet):
    import random
    sql = []
    st = ["address","location","county","age","gender","race","collection","category","result","city","club","year","day","birth Date"]
    x = []
    t = -1
    col = list(test.columns)
    #print("Column order: ", col)
    sql.append("SELECT")
    for i in sherlock_prediction:
        t += 1
        if i in st:
            x.append(t)
    
    #print("Preferred metas found: ", x)
            
    ra = random.choice(x)
    #print("Random choice O/p",ra)
    sql.append(col[ra])
    sql.append("FROM")
    sql.append("test")
    sql.append("WHERE")
    guess5 = random.randint(0,len(col)-1)
    while guess5 == ra:
        guess5 = random.randint(0,len(col)-1)
    sql.append(col[guess5])
    #print("SQL output ",sql)
    checker = sherlock_prediction[guess5]
    selection = sqlcheatsheet[sqlcheatsheet['Category'] == checker]
    selection = selection.loc[:, (selection != 0).any(axis=0)]
    selection = selection.drop(columns = ['Category'])
    map_col = list(selection.columns)
    #print("Map Col output ",map_col)
    if(len(map_col) == 3):
        guess2 = random.randint(0,len(map_col)-2)
    else:
        guess2 = random.randint(2,len(map_col)-1)
    sql.append(map_col[guess2])
    guess3 = random.randint(0,len(test[col[guess5]])-1)
    value = test[col[guess5]].iloc[guess3]
    sql.append(value)
    #print("SQL output ",sql)
    

    
    return sql
# changes to original - give specific step by step instructions to GPT to 
# make changes correctly and then test them
