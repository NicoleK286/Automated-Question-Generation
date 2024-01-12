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


def ques(sql,col,df,sher_pred):
    name2 = sql[5]
    
    #print("Column names in 'col' DataFrame:")
    #print(col['Column'].tolist())
    
    name1 = sql[1]
    #print("1st column:", name1)
    #print("2nd column:", name2)
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
    des1_para = preprocess_input_text(des1_para)
    
    des2_para = get_response(des2, 1)[0]
    des2_para = preprocess_input_text(des2_para)

    # Remove periods from des1_para and des2_para
    des1_para = des1_para.replace('.', '')
    des2_para = des2_para.replace('.', '')

    if (sql[6] == "Minimum"):
        a1 = random.randint(0, 1)
        guess1 = random.randint(0, len(df[sql[1]]) - 1)
        value1 = df[sql[1]].iloc[guess1]
        if a1 == 1:
            template = "What is the lowest value of {} where {} is equal to {} in the data?"
            q1 = template.format(sql[5], sql[1], str(value1))
            que = template.format(des2, des1, str(value1))
            que2 = template.format(des2_para, des1_para, str(value1))

        else:
            template = "Which {} has the least {} within the data?"
            q1 = template.format(sql[1], sql[5])
            que = template.format(des1, des2)
            que2 = template.format(des1_para, des2_para)


    elif (sql[6] == "Maximum"):
        a2 = random.randint(0,1)
        guess2 = random.randint(0,len(df[sql[1]])-1)
        value2 = df[sql[1]].iloc[guess2]
        if a2 == 1:
            template = "What is the highest value of {} where {} is equal to {} in the data?"
            q1 = template.format(sql[5], sql[1], str(value2))
            que = template.format(des2, des1, str(value2))
            que2 = template.format(des2_para, des1_para, str(value2))

        else:
            template = "Which {} has the highest {} within the data?"
            q1 = template.format(sql[1], sql[5])
            que = template.format(des1, des2)
            que2 = template.format(des1_para, des2_para)


    elif (sql[6] == "Average "):
        a3 = random.randint(0,1)
        if a3 == 1:
            template = "Which records of {} have averages for {} that are lower than {} in the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))
        else:
            template = "Which records of {} have averages for {} that are higher than {} in the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))            

                
    elif (sql[6] == "COUNT"):
        template = "For a given value of {}, what are the total number of records for {}, within the dataset?"
        q1 = template.format(sql[1], sql[5])
        que = template.format(des1, des2)
        que2 = template.format(des1_para, des2_para)

            
    elif (sql[6] == "Equal to"):
        r = random.randint(0, 1)
        if r == 0:
            template = "Which {} has {} equal to {} in the dataset?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))
                 
        else:
            template = "What is the value of {} where {} is equal to {} in the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))              

    elif (sql[6] == "Not Equal to"):
        r = random.randint(0, 1)
        if r == 0:
            template = "How many unique instances of {} occur where {} is not equal to {} in the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))              
                
        else:
            template = "For which records of {} is {} not equal to {} in the dataset?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))              
     

    elif (sql[6] == "Lesser than"):
        r = random.randint(0, 1)
        if r == 0:
            template = "Which instances of {} have {} that are lower than {} in the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))     
                
        else:
            template = "How many records of {} have {} less than {} ,within the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))     

    elif (sql[6] == "Greater than"):
        r = random.randint(0, 1)
        if r == 0:
            template = "Which instances of {} have {} that are higher than {} in the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))     
                
        else:
            template = "How many records of {} have {} greater than {} ,within the data?"
            q1 = template.format(sql[1], sql[5], str(sql[7]))
            que = template.format(des1, des2, str(sql[7]))
            que2 = template.format(des1_para, des2_para, str(sql[7]))     

    

    #print("q1:", q1) 
    q1 = preprocess_input_text(str(q1))
    que = preprocess_input_text(str(que))
    que2 = preprocess_input_text(str(que2))
    para = get_response(str(que), 1)
    para = preprocess_input_text(str(para))
    para2 = get_response(str(que2), 1)
    para2 = preprocess_input_text(str(para2))

    print("Template:", q1)
    #print("This is the OG qs:", que)
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
