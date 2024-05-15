def ques(sql,col,df,sher_pred):
    import random
    
    import nltk
    #nltk.download('punkt')
    from nltk.tokenize import word_tokenize
    from nltk.corpus import wordnet as wn
    
    def paraphrase(sentence):
        words = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words)
        paraphrases = []
        for word, tag in pos_tags:
            if tag.startswith("NN") or tag.startswith("VB") or tag.startswith("JJ"):
                synsets = wn.synsets(word, pos=tag[0].lower())
                if synsets:
                    synset = synsets[0]
                    lemma = synset.lemmas()[0]
                    if lemma:
                        paraphrase = lemma.name().replace("_", " ")
                        if paraphrase != word:
                            new_words = words[:]
                            new_words[new_words.index(word)] = paraphrase
                            paraphrase_sentence = " ".join(new_words)
                            paraphrases.append(paraphrase_sentence)
        if paraphrases:
            return random.choice(paraphrases)
        else:
            return sentence



    questions = []
    paraphrased_questions = []
    
    #print(sql)
    name = sql[5]
    
    x = col[col["Column"] == name]
    #print("Col name ques ",x)
    des = x["Description1"].tolist()[0]
    #print("Col Des ques ",des)
    col1 = list(df.columns)
    #print ("Column Order: ",col1)  # Same order as that seen in newcolcheck

    if "*" in sql:
        qs = "Show all the records where", des, "are", sql[6],sql[7],"?"
        questions.append(qs) 
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
                    qs = 'In which year', des1, 'was maximum'
                    questions.append(qs)
                elif a3 == 1:
                    qs = 'In which year', des1, 'was minimum'
                    questions.append(qs)            
                elif a3 == 2:
                    qs = 'In which year', des1, 'was below average'
                    questions.append(qs)
                else:
                    qs = 'In which year', des1, 'was above average'
                    questions.append(qs)
        else:
            if (sql[6] == "Minimum"):
                a1 = random.randint(0,1)
                if a1 == 1:
                    ques = "What is the minimum " + des + " among all " + des1 + " ?"
                    qs = ques
                    questions.append(qs)                    
                else:
                    ques = "Which "+ des1 + " has the least "+ des + " ?"
                    qs = ques
                    questions.append(qs)                    
            elif (sql[6] == "Maximum"):
                a2 = random.randint(0,1)
                if a2 == 1:
                    ques = "What is the maximum "+des+" among all "+des1
                    qs = ques
                    questions.append(qs)                    
                else:
                    ques = "Which "+des1+" has the highest "+des+" ?"
                    qs = ques                      
            elif (sql[6] == "Average "):
                r1 = random.randint(0,1)
                if r1 == 0:
                    qs = "What is the average",des,"among all",des1
                    questions.append(qs)
                    ans = df[name].mean()                    

            else:
                import random
                r = random.randint(0,1)
                if r == 0:
                    qs = "Which",des1, "has",des ,sql[6],sql[7], "?"
                    questions.append(qs)                    
                    if(sql[6] == "Equal to"):
                        ans = df[df[name] == sql[7]][name1]
                    elif (sql[6] == "Not Equal to"):
                        ans = df[df[name] != sql[7]][name1]
                    elif (sql[6] == "Lesser than"):
                        ans = df[df[name] < sql[7]][name1]
                    else:
                        ans = df[df[name] > sql[7]][name1]
                else:
                    qs = "What is the", des1 , "where", des  ,sql[6], sql[7], "?"
                    questions.append(qs)                  
                    if(sql[6] == "Equal to"):
                        ans = df[df[name] == sql[7]][name1]
                    elif (sql[6] == "Not Equal to"):
                        ans = df[df[name] != sql[7]][name1]
                    elif (sql[6] == "Lesser than"):
                        ans = df[df[name] < sql[7]][name1]
                    else:
                        ans = df[df[name] > sql[7]][name1]
    
    for question in questions:
        paraphrase = paraphrase(question)
        paraphrased_questions.append(paraphrase)
        print("Original Question:", question)
        print("Paraphrased Question:", paraphrase)

        
        
        
