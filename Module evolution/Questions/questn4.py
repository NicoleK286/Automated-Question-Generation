from para2 import *
import warnings

def ques(sql,col,df,sher_pred):
    import random
    name2 = sql[5]
    
    x = col[col["Column"] == name2]
    des = x["Description1"].tolist()[0]
    col1 = list(df.columns)

    if "*" in sql:
        print("Show all the records where", des, "are", sql[6], sql[7], "?")
    else:
        name1 = sql[1]
        print("1st column:", name1)
        print("2nd column:", name2)
        print("SQL String:", sql)
        x1 = col[col["Column"] == name1]
        des1 = x1["Description1"].tolist()[0]
        if (sql[6] == "Minimum"):
            a1 = random.randint(0,1)
            if a1 == 1:
                que = "What is the minimum " + des + " among all " + des1 + " ?"
                print("What is the minimum des among all des1 ?")
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
            else:
                que = "Which "+ des1 + " has the least "+ des + " ?"
                print("What is the minimum des among all des1 ?")
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
        elif (sql[6] == "Maximum"):
            a2 = random.randint(0,1)
            if a2 == 1:
                que = "What is the maximum "+des+" among all "+des1
                print("What is the maximum des among all des1")
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
            else:
                que = "Which "+des1+" has the highest "+des+" ?"
                print("Which des1 has the highest des")
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
        elif (sql[6] == "Average "):
            r1 = random.randint(0,1)
            if r1 == 0:
                print("What is the average des among all des1")
                que = "What is the average", des, "among all", des1
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
            else:
                guess = random.randint(0,len(df[sql[5]])-1)
                value = df[sql[5]].iloc[guess]
                guess1 = random.randint(0,len(df[sql[5]])-1)
                value1 = df[sql[5]].iloc[guess1]
                print("What is the average", des, "where", des1, "is between", value, "and", value1)
                que = "What is the average", des, "where", des1, "is between", value, "and", value1
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
                
        elif (sql[6] == "COUNT"):
            guess = random.randint(0,len(df[sql[5]])-1)
            value = df[sql[5]].iloc[guess]
            print("How many instances in the record has", des, "with a value of", value, "for", des1, "?")
            que = "How many instances in the record has", des, "with a value of", value, "for", des1, "?"
            print("This is the OG qs:", que)
            stqs = str(que)
            para = get_response(stqs, 1)
            print("This is a paraphrased qs:", para)
            print("")
            
            
        elif (sql[6] == "Sum of"):
            guess = random.randint(0,len(df[sql[5]])-1)
            value = df[sql[5]].iloc[guess]
            guess1 = random.randint(0,len(df[sql[5]])-1)
            value1 = df[sql[5]].iloc[guess1]
            print("What is the sum of", des, "where", des1, "is between", value, "and", value1)
            que = "What is the sum of", des, "where", des1, "is between", value, "and", value1
            print("This is the OG qs:", que)
            stqs = str(que)
            para = get_response(stqs, 1)
            print("This is a paraphrased qs:", para)
            print("")

        elif (sql[6] == "Equal to"):
            r = random.randint(0, 1)
            if r == 0:
                print("Which", des1, "has", des, "equal to", sql[7], "?")
                que = "Which " + des1 + " has " + des + " equal to " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
                
            else:
                print("What is the", des1, "where", des, "is equal to", sql[7], "?")
                que = "What is the " + des1 + " where " + des + " is equal to " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
                

        elif (sql[6] == "Not Equal to"):
            r = random.randint(0, 1)
            if r == 0:
                print("Which", des1, "has", des, "not equal to", sql[7], "?")
                que = "Which " + des1 + " has " + des + " not equal to " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
                
            else:
                print("What is the", des1, "where", des, "is not equal to", sql[7], "?")
                que = "What is the " + des1 + " where " + des + " is not equal to " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
	        

        elif (sql[6] == "Lesser than"):
            r = random.randint(0, 1)
            if r == 0:
                print("Which", des1, "has", des, "is lesser than", sql[7], "?")
                que = "Which " + des1 + " has " + des + " is lesser than " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
                
            else:
                print("What is the", des1, "where", des, "is lesser than", sql[7], "?")
                que = "What is the " + des1 + " where " + des + " is lesser than " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")

        elif (sql[6] == "Greater than"):
            r = random.randint(0, 1)
            if r == 0:
                print("Which", des1, "has", des, "is greater than", sql[7], "?")
                que = "Which " + des1 + " has " + des + " is greaterthan " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
                
            else:
                print("What is the", des1, "where", des, "is greater than", sql[7], "?")
                que = "What is the " + des1 + " where " + des + " is greater than " + str(sql[7]) + "?"
                print("This is the OG qs:", que)
                stqs = str(que)
                para = get_response(stqs, 1)
                print("This is a paraphrased qs:", para)
                print("")
