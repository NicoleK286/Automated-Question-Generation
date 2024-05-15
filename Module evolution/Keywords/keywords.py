def key(file):
    import gensim
    from gensim.utils import simple_preprocess
    from gensim.parsing.preprocessing import STOPWORDS
    import re
    with open(file) as f:
        first_line = f.readline()
#Scope optimization: List the strings we want to remove in the list and then pass it into the list
    first_line = first_line.replace(',', '')
    first_line = first_line.replace('.', '')
    first_line = first_line.replace('\n','')
    first = first_line.replace('-', ' ').split(' ')
    first = [x.lower() for x in first]
    from nltk.corpus import stopwords
    title = [word for word in first if word not in stopwords.words('english')]
    corpus = gensim.corpora.textcorpus.TextCorpus(file)
    model = gensim.models.LdaModel(corpus, id2word=corpus.dictionary,
                               alpha='auto',
                               num_topics=10,
                               passes=10)
    top = model.print_topics()
    topics = []
    for i in range(0,10):
        listToStr = ' '.join([str(elem) for elem in top[i]])
        res = re.findall(r'\w+', listToStr)
        line = re.sub("[^A-Za-z]", " ", listToStr.strip())
        words = line.split()
        topics.append(words)
    total = 0
    maxx = 0
    save = []
    for i in range(0,10):
        total = 0
        for j in topics[i]:
            if j in title:
                total += 1
        if maxx == 0:
            maxx = total
            save.append(i)
        else:
            if total >= maxx:
                maxx = total
                save.append(i)

    temp = []
    for i in save:
        for j in topics[i]:
            temp.append(j)
        
    main = []
    for i in temp:
        if i not in main:
            main.append(i)
        
    extract = []
    for w in main:
        if w in title:
            extract.append(w)

    return extract
    #import random


    #if len(extract) >=3:
     #   print("Enter the number of words in theme <= ", len(extract))
      #  sel = int(input(""))
       # if(sel <= len(extract)):
        #    print(random.sample(extract,sel))
        #else:
         #   print("Wrong Entry")

    #else:
     #   print(extract)
      #  print(random.sample(main,2))