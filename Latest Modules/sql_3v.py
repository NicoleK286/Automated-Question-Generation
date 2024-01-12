import random
from itertools import permutations, product

def sqlqueryv3(test, sherlock_prediction, sqlcheatsheet):
    sql = []
    col = list(test.columns)
    
    # Define the meta category lists
    meta_category_lists = {
        "date": ["birth Date", "day"],
        "loc": ["address", "area", "birth place", "city", "continent", "country", "location", "region", "county"],
        "prf": ["artist", "creator","director","jockey", "operator", "owner", "person", "education", "industry", "publisher", "service", "manufacturer"],
        "cat": ["affiliate", "affiliation", "album", "brand", "capacity", "category", "classification", "club", "code", "command", "collection",
                "company", "component", "currency", "credit", "description", "family", "format", "gender", "genre", "isbn", "language", "name", "nationality",
                "notes", "order", "organisation", "origin", "plays", "product", "range", "requirement", "religion", "result", "sex", "species",
                "state", "status", "team", "team Name", "type"],
        "num": ["age", "class", "depth", "duration", "elevation", "file Size", "grades", "position", "rank", "sales", "symbol", "weight", "ranking"],
        "year": ["year"]
    }
    


    # Define the metacategory groups
    meta_category_groups = ["num", "cat", "prf", "loc", "date", "year"]

    # Generate all possible 3-column combinations without repeats
    #combinations_no_repeats = list(permutations(meta_category_groups, 3))

    # Generate all possible 3-column combinations with repeats of "num" and "cat" types
    #repeat_combinations = list(product(meta_category_groups, repeat=3))

    addn_combinations = [
        ("date", "num", "num"),("year", "num", "num"),("loc", "num", "num"),("prf", "num", "num"),("cat", "num", "num"),
        ("date", "cat", "cat"),("year", "cat", "cat"),("loc", "cat", "cat"),("prf", "cat", "cat"),("num", "cat", "cat"),
        ("date", "num", "cat"),("year", "num", "cat"),("loc", "num", "cat"),("prf", "num", "cat"),
        ("date", "num", "loc"), ("year", "num", "loc"),("loc", "num", "date"),("loc", "num", "year")
    ]

    combinations = addn_combinations
    
    #combinations_no_repeats + repeat_combinations + addn_combinations

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
    
    try:
        sql.append("SELECT")
        
        # Check if the chosen combination is possible
        valid_combination = False
        
        while not valid_combination:
            # Check if there are columns in the first category of the chosen combination
            available_columns_1 = [col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[0]]
            
            # Check if there are columns in the second category of the chosen combination
            available_columns_2 = [col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[1]]

            # Check if there are columns in the second category of the chosen combination
            available_columns_3 = [col_idx for col_idx, group in enumerate(categorized_groups) if group == chosen_combination[2]]
            
            if available_columns_1 and available_columns_2:
                # Randomly select a column from each category
                column_idx_1 = random.choice(available_columns_1)
                column_idx_2 = random.choice(available_columns_2)
                column_idx_3 = random.choice(available_columns_3)
                
                # Check if the columns are different
                if column_idx_1 != column_idx_2 and column_idx_2 != column_idx_3 and column_idx_1 != column_idx_3:
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
        if 'Category' in selection.columns:
            selection = selection.drop(columns=['Category'])

        map_col = list(selection.columns)   
        chosen_map_col_index = random.randint(0, len(map_col) - 1)
        chosen_map_col = map_col[chosen_map_col_index]
        
        guess3 = random.randint(0, len(test[col[column_idx_2]]) - 1)
        value = test[col[column_idx_2]].iloc[guess3]
        sql.extend([chosen_map_col, value])

        sql.append("AND")  # Add WHERE statement
        sql.append(col[column_idx_3])


        checker3 = sherlock_prediction[column_idx_3]
        selection3 = sqlcheatsheet[sqlcheatsheet['Category'] == checker3]
        selection3 = selection3.loc[:, (selection3 != 0).any(axis=0)]
        
        if 'Category' in selection3.columns:
            selection3 = selection3.drop(columns=['Category'])

        map_col3= list(selection3.columns)   
        chosen_map_col_index3 = random.randint(0, len(map_col3) - 1)
        chosen_map_col3 = map_col[chosen_map_col_index3]

        guess4 = random.randint(0, len(test[col[column_idx_3]]) - 1)
        value3 = test[col[column_idx_3]].iloc[guess4]
        sql.extend([chosen_map_col3, value3])

    except IndexError:
        # Handle the case where choosing from an empty sequence
        #print("Skipping SQL string due to an empty sequence.")
        pass  # You might want to return a special value or None to indicate skipping
     

    return sql

# col1 - sql[1] , col2 - sql[5], col3 - sql[9]
# operator for col 2 - sql[6] , operator for col 3 - sql[10]
# value for col 2 - sql[7] , value for col 3 - sql[11]


    # Define combinations of metacategory lists
#    addn_combinations = [
#        ("date", "num", "num"),("year", "num", "num"),("loc", "num", "num"),("prf", "num", "num"),("cat", "num", "num"),
#        ("date", "cat", "cat"),("year", "cat", "cat"),("loc", "cat", "cat"),("prf", "cat", "cat"),("num", "cat", "cat"),
#        ("date", "num", "cat"),("year", "num", "cat"),("loc", "num", "cat"),("prf", "num", "cat"),
#        ("date", "num", "loc"), ("year", "num", "loc"),("loc", "num", "date"),("loc", "num", "year")
#    ]

