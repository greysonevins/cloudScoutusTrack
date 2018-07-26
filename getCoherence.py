import pandas as pd
from ast import literal_eval
from gensim import corpora
import gensim
from gensim.models import CoherenceModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#
# chunksize =  10**8
#
# tweets2 = pd.DataFrame()
# def getTweets():
#     for chunk in pd.read_csv("finalTweets_LDA.csv", index_col=0,  engine='python', chunksize=chunksize):
#         yield chunk
#
#
# tweets2 = tweets2.append(list(getTweets()))
# tweets2["Clean_Words_TM"] = tweets2["Clean_Words_TM"].apply(lambda text: literal_eval(text))


# store = pd.HDFStore('store.h5')
# tweets2 = store["tweetsDf"]
# dictionary = corpora.Dictionary(tweets2["Clean_Words_TM"])
# corpus = [dictionary.doc2bow(text) for text in tweets2["Clean_Words_TM"]]
#
#
# mallet_path = "/home/Greyson/mallet-2.0.8/bin/mallet"
# def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
#     """
#     Compute c_v coherence for various number of topics
#
#     Parameters:
#     ----------
#     dictionary : Gensim dictionary
#     corpus : Gensim corpus
#     texts : List of input texts
#     limit : Max num of topics
#
#     Returns:
#     -------
#     model_list : List of LDA topic models
#     coherence_values : Coherence values corresponding to the LDA model with respective number of topics
#     """
#     coherence_values = []
#     model_list = []
#     for num_topics in range(start, limit, step):
#         model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
#         model_list.append(model)
#         coherencemodel = CoherenceModel(model=model, corpus=corpus,texts=tweets2["Clean_Words_TM"],  dictionary=dictionary, coherence='c_v')
#         coherence_values.append(coherencemodel.get_coherence())
#         print(coherence_values)
#     return model_list, coherence_values
#
#
# model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=tweets2["Clean_Words_TM"], start=2, limit=40, step=4)
coherence_values = [0.2914294448737216, 0.21330388233269973, 0.26615124181394023, 0.26696741698594856, 0.28356585368483844, 0.28719351820801253, 0.285865498978522, 0.29589729776741946, 0.31115197095188396, 0.2865425914534838]

limit=40; start=2; step=4;
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.savefig("coherence.png")

for m, cv in zip(x, coherence_values):
    print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
