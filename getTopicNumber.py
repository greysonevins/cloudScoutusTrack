
#come back here
from gensim import corpora
import pandas as pd
store = pd.HDFStore('store.h5')
tweets2 = store["tweetsDf"]
store.close()

dictionary = corpora.Dictionary(tweets2["Clean_Words_TM"])
corpus = [dictionary.doc2bow(text) for text in tweets2["Clean_Words_TM"]]
import gensim
lda = gensim.models.ldamodel.LdaModel.load('model20.gensim')
import pyLDAvis.gensim


def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        if i%10000 == 0:
            print("Here at {}".format(i))
            print("Progress == {}".format((i/len(ldamodel[corpus]))*100))
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts["Clean_Words_TM"])
    contents_ids = pd.Series(texts.index.values)
    sent_topics_df = pd.concat([sent_topics_df, contents, contents_ids], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=lda, corpus=corpus, texts=tweets2)

# Format
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text', "Text_Index"]

# Show
df_dominant_topic.head(10)
store = pd.HDFStore('store.h5')
store["df_dominant_topic"] = df_dominant_topic
