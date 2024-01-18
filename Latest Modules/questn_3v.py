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
        print(version_scores)
        
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
    print("SQL String:", sql)
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
        if (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            template = "For which records of {}, is {} {} {} and {} is {} {}, in the dataset?"
            q1 = template.format(sql[1],      sql[5],    sql[6], str(sql[7]), sql[9],    sql[10], str(sql[11]))
            que = template.format(des1,       des2,      sql[6], str(sql[7]), des3,      sql[10], str(sql[11]))
            que2 = template.format(des1_para, des2_para, sql[6], str(sql[7]), des3_para, sql[10], str(sql[11]))


        elif (sql[6] == "Average ") and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For which records of {}, is the average of {} lesser than {} and {} is {} {}, within the dataset?"
                q1 = template.format(sql[1],      sql[5],    str(sql[7]), sql[9],    sql[10], str(sql[11]))
                que = template.format(des1,       des2,      str(sql[7]), des3,      sql[10], str(sql[11]))
                que2 = template.format(des1_para, des2_para, str(sql[7]), des3_para, sql[10], str(sql[11]))
            else:
                template = "For which records of {}, is the average of {} higher than {} and {} is {} {}, within the dataset?"
                q1 = template.format(sql[1],      sql[5],    str(sql[7]), sql[9],    sql[10], str(sql[11]))
                que = template.format(des1,       des2,      str(sql[7]), des3,      sql[10], str(sql[11]))
                que2 = template.format(des1_para, des2_para, str(sql[7]), des3_para, sql[10], str(sql[11]))


        elif (sql[6] == "Average ") and (sql[10] in ("Minimum", "Maximum")):
            a3 = random.randint(0,1)
            guess1 = random.randint(0, len(df[sql[1]]) - 1)
            value1 = df[sql[1]].iloc[guess1]
            if a3 == 0:
                template = "When {} is equal to {} and the average of {} is lesser than {}, what is the {} value of {}, within the dataset?"
                q1 = template.format(sql[1],      str(value1), sql[5],    str(sql[7]),  sql[10], sql[9])
                que = template.format(des1,       str(value1), des2,      str(sql[7]),  sql[10], des3)
                que2 = template.format(des1_para, str(value1), des2_para, str(sql[7]),  sql[10], des3_para)
            else:
                template = "When {} is equal to {} and the average of {} {} is higher than {}, what is the {} value of {}, within the dataset?"
                q1 = template.format(sql[1],      str(value1), sql[5],    str(sql[7]),  sql[10], sql[9])
                que = template.format(des1,       str(value1), des2,      str(sql[7]),  sql[10], des3)
                que2 = template.format(des1_para, str(value1), des2_para, str(sql[7]),  sql[10], des3_para)


        elif (sql[6] == "Average ") and (sql[10] in ("Average ")):
            guess2 = random.randint(0, len(df[sql[1]]) - 1)
            value2 = df[sql[1]].iloc[guess2]
            template = "When {} is equal to {}, what are the average values of {} and {}, within the dataset?"
            q1 = template.format(sql[1],      str(value2), sql[5],    sql[9])
            que = template.format(des1,       str(value2), des2,      des3)
            que2 = template.format(des1_para, str(value2), des2_para, des3_para)


        elif (sql[10] == "Average ") and (sql[6] in ("Minimum", "Maximum")):
            a3 = random.randint(0,1)
            guess3 = random.randint(0, len(df[sql[1]]) - 1)
            value3 = df[sql[1]].iloc[guess3]
            if a3 == 0:
                template = "When {} is equal to {} and the average of {} is lesser than {}, what is the {} value of {}, within the dataset?"
                q1 = template.format(sql[1],      str(value3), sql[9],    str(sql[7]),  sql[10], sql[5])
                que = template.format(des1,       str(value3), des3,      str(sql[7]),  sql[10], des2)
                que2 = template.format(des1_para, str(value3), des3_para, str(sql[7]),  sql[10], des2_para)
            else:
                template = "When {} is equal to {} and the average of {} is higher than {}, what is the {} value of {}, within the dataset?"
                q1 = template.format(sql[1],      str(value3), sql[9],    str(sql[7]),  sql[10], sql[5])
                que = template.format(des1,       str(value3), des3,      str(sql[7]),  sql[10], des2)
                que2 = template.format(des1_para, str(value3), des3_para, str(sql[7]),  sql[10], des2_para)


        elif (sql[6] == "Average ") and (sql[10] == "COUNT"):
            a3 = random.randint(0,1)
            guess4 = random.randint(0, len(df[sql[1]]) - 1)
            value4 = df[sql[1]].iloc[guess4]
            if a3 == 0:
                template = "When {} is equal to {} and the average of {} is lesser than {}, how many records of {} are present within the dataset?"
                q1 = template.format(sql[1],      str(value4), sql[5],    str(sql[7]),  sql[9])
                que = template.format(des1,       str(value4), des2,      str(sql[7]),  des3)
                que2 = template.format(des1_para, str(value4), des2_para, str(sql[7]),  des3_para)
            else:
                template = "When {} is equal to {} and the average of {} is higher than {}, how many records of {} are present within the dataset?"
                q1 = template.format(sql[1],      str(value4), sql[5],    str(sql[7]),  sql[9])
                que = template.format(des1,       str(value4), des2,      str(sql[7]),  des3)
                que2 = template.format(des1_para, str(value4), des2_para, str(sql[7]),  des3_para)


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "Average "):
            a3 = random.randint(0,1)
            if a3 == 0:
                template = "For which records of {}, is {} {} {} and the average of {} is lesser than {}, within the dataset?"
                q1 = template.format(sql[1],      sql[5],    sql[6], str(sql[7]), sql[9],    str(sql[11]))
                que = template.format(des1,       des2,      sql[6], str(sql[7]), des3,      str(sql[11]))
                que2 = template.format(des1_para, des2_para, sql[6], str(sql[7]), des3_para, str(sql[11]))
            else:
                template = "For which records of {}, is {} {} {} and the average of {} is higher than {}, within the dataset?"
                q1 = template.format(sql[1],      sql[5],    sql[6], str(sql[7]), sql[9],    str(sql[11]))
                que = template.format(des1,       des2,      sql[6], str(sql[7]), des3,      str(sql[11]))
                que2 = template.format(des1_para, des2_para, sql[6], str(sql[7]), des3_para, str(sql[11]))


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "COUNT"):
            guess5 = random.randint(0, len(df[sql[1]]) - 1)
            value5 = df[sql[1]].iloc[guess5]
            template = "When {} is equal to {} and {} is {} {}, what is the total number of records for {}, in the dataset?"
            q1 = template.format(sql[1],      str(value5), sql[5],    sql[6], str(sql[7]), sql[9]    )
            que = template.format(des1,       str(value5), des2,      sql[6], str(sql[7]), des3      )
            que2 = template.format(des1_para, str(value5), des2_para, sql[6], str(sql[7]), des3_para )

        elif (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[6] == "COUNT"):
            guess6 = random.randint(0, len(df[sql[1]]) - 1)
            value6 = df[sql[1]].iloc[guess6]
            template = "When {} is equal to {} and {} is {} {}, what is the total number of records for {}, in the dataset?"
            q1 = template.format(sql[1],      str(value6), sql[9],    sql[10], str(sql[11]), sql[5]    )
            que = template.format(des1,       str(value6), des3,      sql[10], str(sql[11]), des2      )
            que2 = template.format(des1_para, str(value6), des3_para, sql[10], str(sql[11]), des2_para )


        elif (sql[6] == "COUNT") and (sql[10] == "Minimum"):
            guess7 = random.randint(0, len(df[sql[1]]) - 1)
            value7 = df[sql[1]].iloc[guess7]
            template = "When {} is equal to {}, how many records of {} are present, for the lowest value of {}, in the dataset?"
            q1 = template.format(sql[1],      str(value7), sql[5],    sql[9])
            que = template.format(des1,       str(value7), des2,      des3)
            que2 = template.format(des1_para, str(value7), des2_para, des3_para)
        
        elif (sql[6] == "COUNT") and (sql[10] =="Maximum"):
            guess8 = random.randint(0, len(df[sql[1]]) - 1)
            value8 = df[sql[1]].iloc[guess8]
            template = "When {} is equal to {}, how many records of {} are present, for the highest value of {} in the dataset?"
            q1 = template.format(sql[1],      str(value8), sql[5],    sql[9])
            que = template.format(des1,       str(value8), des2,      des3)
            que2 = template.format(des1_para, str(value8), des2_para, des3_para)


        elif (sql[6] ==  "Minimum") and (sql[10] == "COUNT"):
            guess9 = random.randint(0, len(df[sql[1]]) - 1)
            value9 = df[sql[1]].iloc[guess9]
            template = "When {} is equal to {}, how many records of {} are present, for the lowest value of {} in the dataset?"
            q1 = template.format(sql[1],      str(value9), sql[9],    sql[5])
            que = template.format(des1,       str(value9), des3,      des2)
            que2 = template.format(des1_para, str(value9), des3_para, des2_para)
        

        elif (sql[6] ==  "Maximum") and (sql[10] == "COUNT"):
            guess10 = random.randint(0, len(df[sql[1]]) - 1)
            value10 = df[sql[1]].iloc[guess10]
            template = "When {} is equal to {}, how many records of {} are present, for the highest value of {} in the dataset?"
            q1 = template.format(sql[1],      str(value10), sql[9],    sql[5])
            que = template.format(des1,       str(value10), des3,      des2)
            que2 = template.format(des1_para, str(value10), des3_para, des2_para)

        elif (sql[6] ==  "COUNT") and (sql[10] == "COUNT"):
            guess11 = random.randint(0, len(df[sql[1]]) - 1)
            value11 = df[sql[1]].iloc[guess11]
            template = "When {} is equal to {}, how many records of {} and {} are present, in the dataset?"
            q1 = template.format(sql[1],      str(value11), sql[9],    sql[5])
            que = template.format(des1,       str(value11), des3,      des2)
            que2 = template.format(des1_para, str(value11), des3_para, des2_para)


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "Minimum"):
            guess12 = random.randint(0, len(df[sql[1]]) - 1)
            value12 = df[sql[1]].iloc[guess12]
            template = "When {} is equal to {} and {} is {} {}, what is the lowest value of {}, in the dataset?"
            q1 = template.format(sql[1],      str(value12), sql[5],    sql[6], str(sql[7]), sql[9]    )
            que = template.format(des1,       str(value12), des2,      sql[6], str(sql[7]), des3      )
            que2 = template.format(des1_para, str(value12), des2_para, sql[6], str(sql[7]), des3_para ) 

        elif (sql[6] == "Minimum") and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            guess13 = random.randint(0, len(df[sql[1]]) - 1)
            value13 = df[sql[1]].iloc[guess13]
            template = "When {} is equal to {}, what is the lowest value of {} in the dataset, while {} is {} {}?"
            q1 = template.format(sql[1],      str(value13), sql[5],    sql[9],    sql[10], str(sql[11]))
            que = template.format(des1,       str(value13), des2,      des3,      sql[10], str(sql[11]))
            que2 = template.format(des1_para, str(value13), des2_para, des3_para, sql[10], str(sql[11]))


        elif (sql[6] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")) and (sql[10] == "Maximum"):
            guess14 = random.randint(0, len(df[sql[1]]) - 1)
            value14 = df[sql[1]].iloc[guess14]
            template = "When {} is equal to {}, where {} is {} {}, what is the highest value of {}, in the dataset?"
            q1 = template.format(sql[1],      str(value14), sql[5],    sql[6], str(sql[7]), sql[9]    )
            que = template.format(des1,       str(value14), des2,      sql[6], str(sql[7]), des3      )
            que2 = template.format(des1_para, str(value14), des2_para, sql[6], str(sql[7]), des3_para )

        elif (sql[6] == "Maximum") and (sql[10] in ("Equal to", "Not Equal to", "Lesser than", "Greater than")):
            guess15 = random.randint(0, len(df[sql[1]]) - 1)
            value15 = df[sql[1]].iloc[guess15]
            template = "When {} is equal to {}, what is the highest value of {} in the dataset, when {} is {} {}?"
            q1 = template.format(sql[1],      str(value15), sql[5],    sql[9],    sql[10], str(sql[11]))
            que = template.format(des1,       str(value15), des2,      des3,      sql[10], str(sql[11]))
            que2 = template.format(des1_para, str(value15), des2_para, des3_para, sql[10], str(sql[11]))

        elif (sql[6] in ("Minimum", "Maximum")) and (sql[10] in ("Minimum", "Maximum")):
            if (sql[6]=="Minimum") and (sql[10]=="Maximum"):
                template = "How many records of {} are present within the data, where {} has the lowest value and {} has the highest value?"
                q1 = template.format(sql[1],      sql[5],    sql[9]    )
                que = template.format(des1,       des2,      des3      )
                que2 = template.format(des1_para, des2_para, des3_para )
            elif (sql[6]=="Maximum") and (sql[10]=="Minimum"):
                template = "How many records of {} are present within the data, where {} has the highest value and {} has the lowest value?"
                q1 = template.format(sql[1],      sql[5],    sql[9]    )
                que = template.format(des1,       des2,      des3      )
                que2 = template.format(des1_para, des2_para, des3_para )
            elif (sql[6]=="Minimum") and (sql[10]=="Minimum"):
                template = "How many records of {} are present within the data, where {} and {} have the lowest values in the dataset?"
                q1 = template.format(sql[1],      sql[5],    sql[9]    )
                que = template.format(des1,       des2,      des3      )
                que2 = template.format(des1_para, des2_para, des3_para )
            elif (sql[6]=="Maximum") and (sql[10]=="Maximum"):
                template = "How many records of {} are present within the data, where {} and {} have the highesy values in the dataset?"
                q1 = template.format(sql[1],      sql[5],    sql[9]    )
                que = template.format(des1,       des2,      des3      )
                que2 = template.format(des1_para, des2_para, des3_para )

    except IndexError:
        # Handle the case where choosing from an empty sequence
        #print("Skipping Question due to an empty sequence.")
        return None  # You might want to return a special value or None to indicate skipping


    print("Template:", q1) 
    q1 = preprocess_input_text(str(q1))
    que = preprocess_input_text(str(que))
    que2 = preprocess_input_text(str(que2))
    para = get_response(str(que), 1)
    para = preprocess_input_text(str(para))
    para2 = get_response(str(que2), 1)
    para2 = preprocess_input_text(str(para2))

    #print("Template:", q1)
    print("This is the OG qs:", que)
    #print("This is a PP qs:", para)
    #print("This is the colPP qs:", que2)
    #print("This is a colPP para qs:", para2)
    print("")
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
