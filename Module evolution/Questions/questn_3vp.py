from para7 import preprocess_input_text, get_response
import pandas as pd
import requests
import random

def check_grammar(text):
    # LanguageTool API endpoint
    api_url = 'https://languagetool.org/api/v2/check'

    # Set the language
    language = 'en-US'

    # Prepare the request payload
    data = {
        'language': language,
        'text': text
    }

    try:
        # Make the request to LanguageTool API
        response = requests.post(api_url, data=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        results = response.json()

        # Set a threshold for the number of allowed grammar errors
        max_allowed_errors = 3

        # Calculate grammatical correctness score
        num_errors = len(results.get('matches', []))
        correctness_score = 1 - min(num_errors / max_allowed_errors, 1.0)

        return correctness_score

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return 0  # Return a low score in case of an error

# Declare the preference order
preference_order = [1, 0, 3, 2, 4]

def score_question_grammar(questions):
    # Use check_grammar function to filter questions based on grammatical accuracy
    filtered_questions = [question for question in questions if check_grammar(question)]
    
    # If there are filtered questions, score them based on the original criteria
    if filtered_questions:
        # Enumerate through each version to get scores
        scores = [check_grammar(question) for question in filtered_questions]
        
        # Create a dictionary to store scores for each version
        version_scores = dict(zip(range(len(scores)), scores))
        #print(version_scores)
        
        # Find the highest score
        highest_score = max(scores)
        
        # Get indices of versions with the highest score
        best_version_indices = [index for index, score in enumerate(scores) if score == highest_score]
        
        # Sort the indices based on preference order
        best_version_indices.sort(key=lambda x: preference_order.index(x))
        
        # Choose the first index as the best version
        best_version_index = best_version_indices[0]
        
        # Return both the scores and the index of the best version as a tuple
        return scores, best_version_index
    else:
        # If no filtered questions, return -1 or handle accordingly
        return -1


def quesv3(sql,col,df,sher_pred):
    name2 = sql[5]
    name3 = sql[9]
    #print("Column names in 'col' DataFrame:")
    #print(col['Column'].tolist())
    
    name1 = sql[1]
    #print("1st column:", name1)
    #print("2nd column:", name2)
    #print("3rd column:", name3)
    print("Query String:", sql)
    x1 = col[col["Column"] == name1]
    if not x1.empty and not pd.isna(x1["Description1"].iloc[0]):
        des1= x1["Description1"].iloc[0]
    else:
        des1= "Description not available"
        
    
    x2 = col[col["Column"] == name2]
    if not x2.empty and not pd.isna(x2["Description1"].iloc[0]):
        des2 = x2["Description1"].iloc[0]
    else:
        des2 = "Description not available"

    x3 = col[col["Column"] == name3]
    if not x3.empty and not pd.isna(x3["Description1"].iloc[0]):
        des3 = x3["Description1"].iloc[0]
    else:
        des3 = "Description not available"
		
    col1 = list(df.columns)


    # Paraphrase des1 and des2
    des1_para = get_response(des1, 1)[0]
    des1_para = preprocess_input_text(des1_para)
    
    des2_para = get_response(des2, 1)[0]
    des2_para = preprocess_input_text(des2_para)

    des3_para = get_response(des3, 1)[0]
    des3_para = preprocess_input_text(des3_para)

    # Remove periods from des1_para and des2_para
    des1_para = des1_para.replace('.', '')
    des2_para = des2_para.replace('.', '')
    des3_para = des3_para.replace('.', '')
    
    try:
        guess1 = random.randint(0, len(df[sql[1]]) - 1)
        value1 = df[sql[1]].iloc[guess1]
        if (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            template = "Which area in {} {}, has {} {} {} and {} {} {}, in the dataset?"
            q1 = template.format(str(value1),  sql[1],      sql[5],    sql[6], str(sql[7]), sql[9],    sql[10], str(sql[11]))
            que = template.format(str(value1), des1,       des2,      sql[6], str(sql[7]), des3,      sql[10], str(sql[11]))
            que2 = template.format(str(value1), des1_para, des2_para, sql[6], str(sql[7]), des3_para, sql[10], str(sql[11]))


        elif (sql[6] == "Average ") and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "Which area in {} {}, has average of {} lesser than {} and {} {} {}, within the dataset?"
            else:
                template = "Which area in {} {}, has average of {} higher than {} and {} {} {}, within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    str(sql[7]), sql[9],    sql[10], str(sql[11]))
            que = template.format(str(value1), des1,       des2,      str(sql[7]), des3,      sql[10], str(sql[11]))
            que2 = template.format(str(value1), des1_para, des2_para, str(sql[7]), des3_para, sql[10], str(sql[11]))


        elif (sql[6] == "Average ") and (sql[10] in ("Minimum", "Maximum")):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For {} {}, where the average of {} is lesser than {}, what is the {} value of {}, within the dataset?"
            else:
                template = "For {} {}, where the average of {} {} is higher than {}, what is the {} value of {}, within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    str(sql[7]),  sql[10], sql[9])
            que = template.format(str(value1), des1,       des2,      str(sql[7]),  sql[10], des3)
            que2 = template.format(str(value1), des1_para, des2_para, str(sql[7]),  sql[10], des3_para)


        elif (sql[6] == "Average ") and (sql[10] in ("Average ")):
            template = "For {} {}, what are the average values of {} and {}, within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[9])
            que = template.format(str(value1), des1,       des2,      des3)
            que2 = template.format(str(value1), des1_para, des2_para, des3_para)


        elif (sql[10] == "Average ") and (sql[6] in ("Minimum", "Maximum")):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For {} {}, where the average of {} is lesser than {}, what is the {} value of {}, within the dataset?"
            else:
                template = "For {} {}, where the average of {} is higher than {}, what is the {} value of {}, within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[9],    str(sql[11]),  sql[6], sql[5])
            que = template.format(str(value1), des1,       des3,      str(sql[11]),  sql[6], des2)
            que2 = template.format(str(value1), des1_para, des3_para, str(sql[11]),  sql[6], des2_para)


        elif (sql[6] == "Average ") and (sql[10] == "COUNT"):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For {} {}, where the average of {} is lesser than {}, how many records of {} are present within the dataset?"
            else:
                template = "For {} {}, where the average of {} is higher than {}, how many records of {} are present within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    str(sql[7]),  sql[9])
            que = template.format(str(value1), des1,       des2,      str(sql[7]),  des3)
            que2 = template.format(str(value1), des1_para, des2_para, str(sql[7]),  des3_para)


        elif (sql[10] == "Average ") and (sql[6] == "COUNT"):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For {} {}, where the average of {} is lesser than {}, how many records of {} are present within the dataset?"
            else:
                template = "For {} {}, where the average of {} is higher than {}, how many records of {} are present within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[9],    str(sql[11]),  sql[5])
            que = template.format(str(value1), des1,       des3,      str(sql[11]),  des2)
            que2 = template.format(str(value1), des1_para, des3_para, str(sql[11]),  des2_para)


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "Average "):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For which areas in {} {}, is {} {} {} and the average of {} is lesser than {}, within the dataset?"
            else:
                template = "For which areas in {} {}, is {} {} {} and the average of {} is higher than {}, within the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[6], str(sql[7]), sql[9],    str(sql[11]))
            que = template.format(str(value1), des1,       des2,      sql[6], str(sql[7]), des3,      str(sql[11]))
            que2 = template.format(str(value1), des1_para, des2_para, sql[6], str(sql[7]), des3_para, str(sql[11]))


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "COUNT"):
            template = "For {} {}, where {} is {} {}, how many records for {}, are present in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[6], str(sql[7]), sql[9]    )
            que = template.format(str(value1), des1,       des2,      sql[6], str(sql[7]), des3      )
            que2 = template.format(str(value1), des1_para, des2_para, sql[6], str(sql[7]), des3_para )


        elif (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[6] == "COUNT"):
            template = "For {} {}, where {} is {} {}, how many records for {}, are present in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[9],    sql[10], str(sql[11]), sql[5]    )
            que = template.format(str(value1), des1,       des3,      sql[10], str(sql[11]), des2      )
            que2 = template.format(str(value1), des1_para, des3_para, sql[10], str(sql[11]), des2_para )


        elif (sql[6] == "COUNT") and (sql[10] == "Minimum"):
            template = "For {} {}, how many records of {} are present, for the lowest value of {}, in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[9])
            que = template.format(str(value1), des1,       des2,      des3)
            que2 = template.format(str(value1), des1_para, des2_para, des3_para)
        
        elif (sql[6] == "COUNT") and (sql[10] =="Maximum"):
            template = "For {} {}, how many records of {} are present, for the highest value of {} in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[9])
            que = template.format(str(value1), des1,       des2,      des3)
            que2 = template.format(str(value1), des1_para, des2_para, des3_para)


        elif (sql[6] ==  "Minimum") and (sql[10] == "COUNT"):
            template = "For {} {}, how many records of {} are present, for the lowest value of {} in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[9],    sql[5])
            que = template.format(str(value1), des1,       des3,      des2)
            que2 = template.format(str(value1), des1_para, des3_para, des2_para)
        

        elif (sql[6] ==  "Maximum") and (sql[10] == "COUNT"):
            template = "For {} {}, how many records of {} are present, for the highest value of {} in the dataset?"
            q1 = template.format(str(value1), sql[1],     sql[9],    sql[5])
            que = template.format(str(value1), des1,       des3,      des2)
            que2 = template.format(str(value1), des1_para, des3_para, des2_para)

        elif (sql[6] ==  "COUNT") and (sql[10] == "COUNT"):
            template = "For {} {}, how many records of {} and {} are present, in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[9],    sql[5])
            que = template.format(str(value1), des1,       des3,      des2)
            que2 = template.format(str(value1), des1_para, des3_para, des2_para)


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "Minimum"):
            template = "For {} {}, where {} is {} {}, what is the lowest value of {}, in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[6], str(sql[7]), sql[9]    )
            que = template.format(str(value1), des1,       des2,      sql[6], str(sql[7]), des3      )
            que2 = template.format(str(value1), des1_para, des2_para, sql[6], str(sql[7]), des3_para ) 

        elif (sql[6] == "Minimum") and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            template = "For {} {}, what is the lowest value of {} in the dataset, while {} is {} {}?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[9],    sql[10], str(sql[11]))
            que = template.format(str(value1), des1,       des2,      des3,      sql[10], str(sql[11]))
            que2 = template.format(str(value1), des1_para, des2_para, des3_para, sql[10], str(sql[11]))


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "Maximum"):
            template = "For {} {}, where {} is {} {}, what is the highest value of {}, in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[6], str(sql[7]), sql[9]    )
            que = template.format(str(value1), des1,       des2,      sql[6], str(sql[7]), des3      )
            que2 = template.format(str(value1), des1_para, des2_para, sql[6], str(sql[7]), des3_para )

        elif (sql[6] == "Maximum") and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            template = "For {} {}, what is the highest value of {} in the dataset, when {} is {} {}?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[9],    sql[10], str(sql[11]))
            que = template.format(str(value1), des1,       des2,      des3,      sql[10], str(sql[11]))
            que2 = template.format(str(value1), des1_para, des2_para, des3_para, sql[10], str(sql[11]))

        elif (sql[6] in ("Minimum", "Maximum")) and (sql[10] in ("Minimum", "Maximum")):
            if (sql[6]=="Minimum") and (sql[10]=="Maximum"):
                template = "How many records of {} {} are present within the data, where {} has the lowest value and {} has the highest value?"

            elif (sql[6]=="Maximum") and (sql[10]=="Minimum"):
                template = "How many records of {} {} are present within the data, where {} has the highest value and {} has the lowest value?"

            elif (sql[6]=="Minimum") and (sql[10]=="Minimum"):
                template = "How many records of {} {} are present within the data, where {} and {} have the lowest values in the dataset?"

            elif (sql[6]=="Maximum") and (sql[10]=="Maximum"):
                template = "How many records of {} are present within the data, where {} and {} have the highest values in the dataset?"
            q1 = template.format(str(value1), sql[1],      sql[5],    sql[9]    )
            que = template.format(str(value1), des1,       des2,      des3      )
            que2 = template.format(str(value1), des1_para, des2_para, des3_para )

    except IndexError:
        # Handle the case where choosing from an empty sequence
        #print("Skipping Question due to an empty sequence.")
        return None  # You might want to return a special value or None to indicate skipping


    print("Column Name Template:", q1) 
    q1 = preprocess_input_text(str(q1))
    que = preprocess_input_text(str(que))
    que2 = preprocess_input_text(str(que2))
    para = get_response(str(que), 1)
    para = preprocess_input_text(str(para))
    para2 = get_response(str(que2), 1)
    para2 = preprocess_input_text(str(para2))

    #print("Template:", q1)
    print("Column Description Template:", que)
    #print("This is a PP qs:", para)
    #print("This is the colPP qs:", que2)
    #print("This is a colPP para qs:", para2)
    #print("")
    # Generate a list of all versions of the question
    all_versions = [q1, que, para, que2, para2]

    # Score each version for grammar and get the tuple of scores and the index of the best version
    scores, best_version_index = score_question_grammar(all_versions)

    # Store the best version in a new variable
    best_version = all_versions[best_version_index]

    best_version = preprocess_input_text(best_version)

    print("Question:", best_version)
    print("")

    return q1, que, para, que2, para2, best_version
