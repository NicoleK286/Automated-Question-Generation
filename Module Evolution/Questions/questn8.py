from para4 import *
import pandas as pd

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
        r1 = random.randint(0,1)
        if r1 == 0:
            q1 = "What is the average " + sql[5] + " among all " + sql[1] + " ?"
            print("Template: What is the average ", sql[5], " among all ", sql[1], "?")
            que = "What is the average ", des2, " among all ", des1, "?"
            que2 = "What is the average ", des2_para, " among all ", des1_para, "?"
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
            guess = random.randint(0,len(df[sql[5]])-1)
            value = df[sql[5]].iloc[guess]
            guess1 = random.randint(0,len(df[sql[5]])-1)
            value1 = df[sql[5]].iloc[guess1]
            q1 = "What is the average " + sql[1] + " where " + sql[5] + " is between " + str(value) + " and " + str(value1) + " ?"
            print("Template: What is the average ", sql[1], " where ", sql[5], " is between ", value, " and ", value1, "?")
            que = "What is the average ", des1, " where ", des2, " is between ", value, " and ", value1, "?"
            que2 = "What is the average ", des1_para, " where ", des2_para, " is between ", value, " and ", value1, "?"
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
        que = "How many instances in the record has ", des1, " with a value of ", value, " for ", des2, "?"
        que2 = "How many instances in the record has ", des1_para, " with a value of ", value, " for ", des2_para, "?"
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
        que = "What is the sum of ", des1, " where ", des2, " is between ", value, " and ", value1
        que2 = "What is the sum of ", des1_para, " where ", des2_para, " is between ", value, " and ", value1
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
    return q1, que, para, que2, para2
