def sqlquery(test, sherlock_prediction, sqlcheatsheet):
    import random
    sql = []
    col = list(test.columns)
    
    sql.append("SELECT")
    
    # Randomly select two distinct columns
    chosen_cols = random.sample(col, 2)
    
    sql.append(chosen_cols[0])
    sql.append("FROM")
    sql.append("test")
    sql.append("WHERE")
    
    # Randomly select another column for comparison
    guess5 = random.choice([col_idx for col_idx in range(len(col)) if col[col_idx] != chosen_cols[0]])
    
    sql.append(col[guess5])
    
    checker = sherlock_prediction[guess5]
    selection = sqlcheatsheet[sqlcheatsheet['Category'] == checker]
    selection = selection.loc[:, (selection != 0).any(axis=0)]
    selection = selection.drop(columns=['Category'])
    map_col = list(selection.columns)
    
    if len(map_col) == 3:
        chosen_map_col_index = random.randint(0, len(map_col) - 2)
    else:
        chosen_map_col_index = random.randint(2, len(map_col) - 1)
    
    chosen_map_col = map_col[chosen_map_col_index]
    
    guess3 = random.randint(0, len(test[col[guess5]]) - 1)
    value = test[col[guess5]].iloc[guess3]
    
    sql.extend([chosen_map_col, value])
    
    return sql
