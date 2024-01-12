import random
import os

generated_sql = set()

mathematical_operators = {
        "Equal to": "==",
        "Not Equal to": "!=",
        "Lesser than": "<",
        "Greater than": ">",
        "Average ": "AVG",
        "COUNT": "COUNT",
        "Minimum": "MIN",
        "Maximum": "MAX",
        "Sum of": "SUM"
    }

def sqlquery(test, sherlock_prediction, sqlcheatsheet):
    global generated_sql
    
    
    
    sql = []
    col = list(test.columns)
    sql_table = []
    
    # Define the meta category lists
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
    
    # Define combinations of metacategory lists
    combinations = [
        ("date", "num"),("date", "cat"),("date", "loc"),("date", "prf"),
        ("loc", "num"),("loc", "cat"),("loc", "date"),("loc", "year"),("loc", "prf"),
        ("prf", "num"),("prf", "cat"),("prf", "date"),("prf", "year"),("prf", "loc"),
        ("cat", "num"),("cat", "year"),("cat", "loc"),("cat", "date"),("cat", "prf"),
        ("year", "num"),("year", "cat"), ("year", "loc"), ("year", "prf")
    ]
    
    # Categorize sherlock_prediction into one of the groups
    categorized_groups = []
    for pred in sherlock_prediction:
        found = False
        for group, meta_list in meta_category_lists.items():
            if pred in meta_list:
                categorized_groups.append(group)
                found = True
                break
        if not found:
            categorized_groups.append(None)  # If not found in any group
    
    # Determine the metacategory combination
    chosen_combination = random.choice(combinations)
    
    sql.append("SELECT")
    
    # Check if the chosen combination is possible
    valid_combination = False
    
    while not valid_combination:
        # Check if there are columns in the first category of the chosen combination
        available_columns_1 = [col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[0]]
        
        # Check if there are columns in the second category of the chosen combination
        available_columns_2 = [col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[1]]
        
        if not available_columns_1 or not available_columns_2:
            chosen_combination = random.choice(combinations)
            continue
        
        if available_columns_1 and available_columns_2:
            # Randomly select a column from each category
            column_idx_1 = random.choice(available_columns_1)
            column_idx_2 = random.choice(available_columns_2)
            
            # Check if the columns are different
            if column_idx_1 != column_idx_2:
                valid_combination = True
                break
        
        # If the chosen combination is not possible, select a random combination
        chosen_combination = random.choice(combinations)
    
    sql.append(col[column_idx_1])
    sql.append("FROM")
    sql.append("test")
    sql.append("WHERE")  # Add WHERE statement
    sql.append(col[column_idx_2])
    
    
    checker = sherlock_prediction[column_idx_2]
    selection = sqlcheatsheet[sqlcheatsheet['Category'] == checker]
    selection = selection.loc[:, (selection != 0).any(axis=0)]
    selection = selection.drop(columns=['Category'])
    map_col = list(selection.columns)
    
    chosen_map_col_index = random.randint(0, len(map_col) - 1)
    chosen_map_col = map_col[chosen_map_col_index]
    guess3 = random.randint(0, len(test[col[column_idx_2]]) - 1)
    value = test[col[column_idx_2]].iloc[guess3]
    sql.extend([chosen_map_col, value])
       
        
    generated_string = str(' '.join(map(str, sql)))

    while generated_string in generated_sql:
        chosen_combination = random.choice(combinations)
        chosen_combination_index = combinations.index(chosen_combination)
        column_idx_1 = random.choice([col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[0]])
        column_idx_2 = random.choice([col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[1]])
        sql[1] = col[column_idx_1]
        sql[5] = col[column_idx_2]
        checker = sherlock_prediction[column_idx_2]
        selection = sqlcheatsheet[sqlcheatsheet['Category'] == checker]
        selection = selection.loc[:, (selection != 0).any(axis=0)]
        selection = selection.drop(columns=['Category'])
        map_col = list(selection.columns)
        chosen_map_col_index = random.randint(0, len(map_col) - 1)
        chosen_map_col = map_col[chosen_map_col_index]
        guess3 = random.randint(0, len(test[col[column_idx_2]]) - 1)
        value = test[col[column_idx_2]].iloc[guess3]
        sql[6] = chosen_map_col
        mathematical_operators = {
        "Equal to": "==",
        "Not Equal to": "!=",
        "Lesser than": "<",
        "Greater than": ">",
        "Average ": "AVG",
        "COUNT": "COUNT",
        "Minimum": "MIN",
        "Maximum": "MAX",
        "Sum of": "SUM"
        }
        operator_string = mathematical_operators.get(sql[6], sql[6])
        sql[6] = operator_string
        sql[7] = str(sql[7])
        generated_string = ' '.join(map(str, sql))

    generated_sql.add(generated_string)
    sql_table.append(generated_string)
    
    with open("sql_strings_output.txt", "a") as f:
        for item in sql_table:
            f.write("%s\n" % item)
    
    return sql
