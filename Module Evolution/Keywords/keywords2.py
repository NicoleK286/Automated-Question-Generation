def key(file):
    import gensim
    from gensim.utils import simple_preprocess
    from gensim.parsing.preprocessing import STOPWORDS
    import re
    with open(file, encoding='utf-8', errors='ignore') as f:
        content = f.read()
        first_line = content.split('\n')[0]
        first_line = first_line.replace(',', '').replace('.', '').replace('-', ' ')
        first = [x.lower() for x in first_line.split(' ')]
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
