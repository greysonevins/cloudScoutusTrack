import pandas as pd
from ast import literal_eval

chunksize =  10**6

tweets2 = pd.DataFrame()
def getTweets():
    for chunk in pd.read_csv("finalTweets_LDA.csv", index_col=0,  engine='python', chunksize=chunksize):
        yield chunk


tweets2 = tweets2.append(list(getTweets()))
tweets2["Clean_Words_TM"] = tweets2["Clean_Words_TM"].apply(lambda text: literal_eval(text))

from gensim import corpora
dictionary = corpora.Dictionary(tweets2["Clean_Words_TM"])
corpus = [dictionary.doc2bow(text) for text in tweets2["Clean_Words_TM"]]
# import pickle
# pickle.dump(corpus, open('corpus.pkl', 'wb'))
# dictionary.save('dictionary.gensim')


import gensim
NUM_TOPICS = 15
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15, chunksize=100000)
ldamodel.save('model15.gensim')
