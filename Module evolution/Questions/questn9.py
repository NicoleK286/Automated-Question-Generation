from para5 import *
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

    # Make the request to LanguageTool API
    response = requests.post(api_url, data=data)
    results = response.json()

    # Set a threshold for the number of allowed grammar errors
    max_allowed_errors = 3

    # Calculate grammatical correctness score
    num_errors = len(results.get('matches', []))
    correctness_score = 1 - min(num_errors / max_allowed_errors, 1.0)

    return correctness_score

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
        
        # Sort the versions based on scores, in descending order
        sorted_versions = sorted(version_scores, key=version_scores.get, reverse=True)
        print(sorted_versions)
        
        # Assign preference order for versions (higher preference for q1, then que)
        preference_order = [1, 0, 3, 4, 2]  # Change this order based on your preference
        
        # Find the best version considering preference order
        best_version_index = None
        for preference in preference_order:
            if preference in sorted_versions:
                best_version_index = preference
                break
        
        # Return both the scores and the index of the best version as a tuple
        return scores, best_version_index
    else:
        # If no filtered questions, return -1 or handle accordingly
        return -1


def ques(sql,col,df,sher_pred):
    import random
    name2 = sql[5]
    
    #print("Column names in 'col' DataFrame:")
    #print(col['Column'].tolist())
    
    name1 = sql[1]
    print("1st column:", name1)
    print("2nd column:", name2)
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
		
    col1 = list(df.columns)


    # Paraphrase des1 and des2
    des1_para = get_response(des1, 1)[0]
    des2_para = get_response(des2, 1)[0]

    # Remove periods from des1_para and des2_para
    des1_para = des1_para.replace('.', '')
    des2_para = des2_para.replace('.', '')

    if (sql[6] == "Minimum"):
        a1 = random.randint(0,1)
        if a1 == 1:
            q1 = "What is the minimum " + sql[5] + " among all " + sql[1] + " ?"
            print("Template: What is the minimum", sql[5], "among all", sql[1], "?")
            que = "What is the minimum " + des2 + " among all " + des1+ " ?"
            que2 = "What is the minimum " + des2_para + " among all " + des1_para+ " ?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
        else:
            q1 = "Which " + sql[1] + " has the least " + sql[5] + " ?"
            print("Template: Which ", sql[1], " has the least ", sql[5], "?")
            que = "Which "+ des1+ " has the least "+ des2 + " ?"
            que2 = "Which "+ des1_para+ " has the least "+ des2_para + " ?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
    elif (sql[6] == "Maximum"):
        a2 = random.randint(0,1)
        if a2 == 1:
            q1 = "What is the maximum " + sql[5] + " among all " + sql[1] + " ?"
            print("Template: What is the maximum ", sql[5], " among all ", sql[1], "?")
            que = "What is the maximum " + des2 + " among all "+des1
            que2 = "What is the maximum " + des2_para + " among all "+des1_para
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
        else:
            q1 = "Which " + sql[1] + " has the highest " + sql[5] + "?"
            print("Template: Which ", sql[1], " has the highest ", sql[5], "?")
            que = "Which "+des1+" has the highest "+des2+" ?"
            que2 = "Which "+des1_para+" has the highest "+des2_para+" ?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
    elif (sql[6] == "Average "):
        q1 = "What is the average " + sql[5] + " among all " + sql[1] + " ?"
        print("Template: What is the average ", sql[5], " among all ", sql[1], "?")
        que = "What is the average "+ des2+ " among all "+ des1+ "?"
        que2 = "What is the average "+ des2_para+ " among all "+ des1_para+ "?"
        stqs = str(que)
        stqs2 = str(que2)
        para = get_response(stqs, 1)
        para2 = get_response(stqs2, 1)
        print("This is the OG qs:", que)
        print("This is a PP qs:", para)
        print("This is the colPP qs:", que2)
        print("This is a colPP para qs:", para2)
        print("")
                
    elif (sql[6] == "COUNT"):
        guess = random.randint(0,len(df[sql[5]])-1)
        value = df[sql[5]].iloc[guess]
        q1 = "How many instances in the record has " + sql[1] + " with a value of " + str(value) + " for " + sql[5] + " ?"
        print("Template: How many instances in the record has ", sql[1], " with a value of ", value, " for ", sql[5], "?")
        que = "How many instances in the record has "+ des1 + " with a value of "+ str(value) + " for "+ des2 + "?"
        que2 = "How many instances in the record has "+ des1_para + " with a value of "+ str(value) + " for "+ des2_para + "?"
        stqs = str(que)
        stqs2 = str(que2)
        para = get_response(stqs, 1)
        para2 = get_response(stqs2, 1)
        print("This is the OG qs:", que)
        print("This is a PP qs:", para)
        print("This is the colPP qs:", que2)
        print("This is a colPP para qs:", para2)
        print("")
            
            
    elif (sql[6] == "Sum of"):
        guess = random.randint(0,len(df[sql[5]])-1)
        value = df[sql[5]].iloc[guess]
        guess1 = random.randint(0,len(df[sql[5]])-1)
        value1 = df[sql[5]].iloc[guess1]
        q1 = "What is the sum of " + sql[1] + " where " + sql[5] + " is between " + str(value) + " and " + str(value1) + " ?"
        print("Template: What is the sum of ", sql[1], " where ", sql[5], " is between ", value, " and ", value1, "?")
        que = "What is the sum of "+ des1+ " where "+ des2+ " is between "+ str(value)+ " and "+ str(value1)+"?"
        que2 = "What is the sum of "+ des1_para+ " where "+ des2_para+ " is between "+ str(value)+ " and "+ str(value1)+"?"
        stqs = str(que)
        stqs2 = str(que2)
        para = get_response(stqs, 1)
        para2 = get_response(stqs2, 1)
        print("This is the OG qs:", que)
        print("This is a PP qs:", para)
        print("This is the colPP qs:", que2)
        print("This is a colPP para qs:", para2)
        print("")

    elif (sql[6] == "Equal to"):
        r = random.randint(0, 1)
        if r == 0:
            q1 = "Which " + sql[1] + " has " + sql[5] + " equal to " + str(sql[7]) + " ?"
            print("Template: Which ", sql[1], " has ", sql[5], " equal to ", sql[7], "?")
            que = "Which " + des1 + " has " + des2+ " equal to " + str(sql[7]) + "?"
            que2 = "Which " + des1_para + " has " + des2_para+ " equal to " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
                
        else:
            q1 = "What is the " + sql[1] + " where " + sql[5] + " is equal to " + str(sql[7]) + " ?"
            print("Template: What is the ", sql[1], " where ", sql[5], " is equal to ", sql[7], "?")
            que = "What is the " + des1 + " where " + des2+ " is equal to " + str(sql[7]) + "?"
            que2 = "What is the " + des1_para + " where " + des2_para+ " is equal to " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
                

    elif (sql[6] == "Not Equal to"):
        r = random.randint(0, 1)
        if r == 0:
            q1 = "Which " + sql[1] + " has " + sql[5] + " that is not equal to " + str(sql[7]) + " ?"
            print("Template: Which ", sql[1], "has ", sql[5], " that is not equal to ", sql[7], "?")
            que = "Which " + des1 + " has " + des2+ " that is not equal to " + str(sql[7]) + "?"
            que2 = "Which " + des1_para + " has " + des2_para+ " that is not equal to " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
                
        else:
            q1 = "What is the " + sql[1] + " where " + sql[5] + " is not equal to " + str(sql[7]) + "?"
            print("Template: What is the ", sql[1], " where ", sql[5], " is not equal to ", sql[7], "?")
            que = "What is the " + des1 + " where " + des2+ "  is not equal to " + str(sql[7]) + "?"
            que2 = "What is the " + des1_para + " where " + des2_para+ "  is not equal to " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
	        

    elif (sql[6] == "Lesser than"):
        r = random.randint(0, 1)
        if r == 0:
            q1 = "Which " + sql[1] + " has " + sql[5] + " lesser than " + str(sql[7]) + "?"
            print("Template: Which ", sql[1], "has", sql[5], " lesser than ", sql[7], "?")
            que = "Which " + des1 + " has " + des2+ " lesser than " + str(sql[7]) + "?"
            que2 = "Which " + des1_para + " has " + des2_para+ " lesser than " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
                
        else:
            q1 = "What is the " + sql[1] + " where " + sql[5] + " is lesser than " + str(sql[7]) + "?"
            print("Template: What is the ", sql[1], "where", sql[5], "is lesser than ", sql[7], "?")
            que = "What is the " + des1 + " where " + des2+ " is lesser than " + str(sql[7]) + "?"
            que2 = "What is the " + des1_para + " where " + des2_para+ " is lesser than " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")

    elif (sql[6] == "Greater than"):
        r = random.randint(0, 1)
        if r == 0:
            q1 = "Which " + sql[1] + " has ", sql[5] + " greater than " + str(sql[7]) + "?"
            print("Template: Which ", sql[1], "has", sql[5], " greater than ", sql[7], "?")
            que = "Which " + des1 + " has " + des2+ " greater than " + str(sql[7]) + "?"
            que2 = "Which " + des1_para + " has " + des2_para+ " greater than " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
                
        else:
            q1 = "What is the " + sql[1] + " where " + sql[5] + " is greater than " + str(sql[7]) + "?"
            print("Template: What is the ", sql[1], " where ", sql[5], " is greater than ", sql[7], "?")
            que = "What is the " + des1 + " where " + des2+ " is greater than " + str(sql[7]) + "?"
            que2 = "What is the " + des1_para + " where " + des2_para+ " is greater than " + str(sql[7]) + "?"
            stqs = str(que)
            stqs2 = str(que2)
            para = get_response(stqs, 1)
            para2 = get_response(stqs2, 1)
            print("This is the OG qs:", que)
            print("This is a PP qs:", para)
            print("This is the colPP qs:", que2)
            print("This is a colPP para qs:", para2)
            print("")
    
    # Generate a list of all versions of the question
    all_versions = [q1, que, para, que2, para2]

    # Score each version for grammar and get the tuple of scores and the index of the best version
    scores, best_version_index = score_question_grammar(all_versions)

    # Store the best version in a new variable
    best_version = all_versions[best_version_index]

    print("Best Version:", best_version)
    print("")

    return q1, que, para, que2, para2, best_version
