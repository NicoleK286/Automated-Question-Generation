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

    # Generate all possible 3-column combinations with repeats
    combinations = list(product(meta_category_groups, repeat=3))

    addn_combinations = [
        ("date", "num", "num"), ("year", "num", "num"), ("loc", "num", "num"), ("prf", "num", "num"), ("cat", "num", "num"),
        ("date", "cat", "cat"), ("year", "cat", "cat"), ("loc", "cat", "cat"), ("prf", "cat", "cat"), ("num", "cat", "cat"),
        ("date", "num", "cat"), ("year", "num", "cat"), ("loc", "num", "cat"), ("prf", "num", "cat"),
        ("date", "num", "loc"), ("year", "num", "loc"), ("loc", "num", "date"), ("loc", "num", "year")
    ]

    combinations = combinations + addn_combinations

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
            # Check if there are columns in each category of the chosen combination
            available_columns = [
                [col_idx for col_idx, group in enumerate(categorized_groups) if group == cat]
                for cat in chosen_combination
            ]

            if all(available_columns):
                # Randomly select a column from each category
                column_indices = [random.choice(available) for available in available_columns]

                for col_idx in column_indices:
                    sql.append(col[col_idx])

                sql.append("FROM")
                sql.append("test")
                sql.append("WHERE")

                # Add WHERE statements
                for col_idx in column_indices:
                    checker = sherlock_prediction[col_idx]
                    selection = sqlcheatsheet[sqlcheatsheet['Category'] == checker]

                    if not selection.empty:
                        map_col = list(selection.columns)
                        chosen_map_col_index = random.randint(0, len(map_col) - 1)
                        chosen_map_col = map_col[chosen_map_col_index]

                        guess = random.randint(0, len(test[col[col_idx]]) - 1)
                        value = test[col[col_idx]].iloc[guess]
                        sql.extend([chosen_map_col, value])
                    else:
                        # Handle the case where selection is empty
                        pass

                    # Add "AND" between conditions
                    if col_idx != column_indices[-1]:
                        sql.append("AND")

                valid_combination = True

            else:
                # If the chosen combination is not possible, select a random combination
                chosen_combination = random.choice(combinations)

    except IndexError:
        # Handle the case where choosing from an empty sequence
        pass  # You might want to return a special value or None to indicate skipping

    return sql
