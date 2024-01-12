def ques(sql,col,df,sher_pred):
    import random
    #print(sql)
    name = sql[5]
    
    x = col[col["Column"] == name]
    #print("Col name ques ",x)
    des = x["Description1"].tolist()[0]
    #print("Col Des ques ",des)
    col1 = list(df.columns)
    print ("Column Order: ",col1)  # Same order as that seen in newcolcheck

    if "*" in sql:
        print("Show all the records where des are  sql[6],sql[7] ?")
        print("Show all the records where", des, "are", sql[6],sql[7],"?")
    else:
        name1 = sql[1]
        print("1st column: ",name1)
        print("2nd column: ",name)
        print ("SQL String:", sql)
        x1 = col[col["Column"] == name1]
        #print("x1",x1)
        des1 = x1["Description1"].tolist()[0]
        #print("des1", des1)
        if 'year' in sher_pred:
            if 'year' in sql[5]:
                a3 = random.randint(0,3)
                if a3 == 0:
                    print('In which year des1 was maximum')
                    print('In which year', des1, 'was maximum')
                elif a3 == 1:
                    print('In which year des1 was minimum')  
                    print('In which year', des1, 'was minimum')            
                elif a3 == 2:
                    print('In which year des1 was below average')
                    print('In which year', des1, 'was below average')
                else:
                    print('In which year des1 was above average')
                    print('In which year', des1, 'was above average')
        else:
            if (sql[6] == "Minimum"):
                a1 = random.randint(0,1)
                if a1 == 1:
                    ques = "What is the minimum " + des + " among all " + des1 + " ?"
                    print("What is the minimum  des among all des1 ?") 
                    print(ques)                    
                else:
                    ques = "Which "+ des1 + " has the least "+ des + " ?"
                    print("What is the minimum  des among all des1 ?") 
                    print(ques)                    
            elif (sql[6] == "Maximum"):
                a2 = random.randint(0,1)
                if a2 == 1:
                    ques = "What is the maximum "+des+" among all "+des1
                    print("What is the maximum des among all des1") 
                    print(ques)                    
                else:
                    ques = "Which "+des1+" has the highest "+des+" ?"
                    print("Which des1 has the highest des")
                    print(ques)                      
            elif (sql[6] == "Average "):
                r1 = random.randint(0,1)
                if r1 == 0:
                    print("What is the average des among all des1")
                    print("What is the average",des,"among all",des1)
                    ans = df[name].mean()                    

            else:
                import random
                r = random.randint(0,1)
                if r == 0:
                    print("Which des1 has des sql[6] sql[7] ?")  
                    print("Which",des1, "has",des ,sql[6],sql[7], "?")                    
                    if(sql[6] == "Equal to"):
                        ans = df[df[name] == sql[7]][name1]
                    elif (sql[6] == "Not Equal to"):
                        ans = df[df[name] != sql[7]][name1]
                    elif (sql[6] == "Lesser than"):
                        ans = df[df[name] < sql[7]][name1]
                    else:
                        ans = df[df[name] > sql[7]][name1]
                else:
                    print("What is the des1 where des, sql[6], sql[7]?")  
                    print("What is the", des1 , "where", des  ,sql[6], sql[7], "?")                  
                    if(sql[6] == "Equal to"):
                        ans = df[df[name] == sql[7]][name1]
                    elif (sql[6] == "Not Equal to"):
                        ans = df[df[name] != sql[7]][name1]
                    elif (sql[6] == "Lesser than"):
                        ans = df[df[name] < sql[7]][name1]
                    else:
                        ans = df[df[name] > sql[7]][name1]
