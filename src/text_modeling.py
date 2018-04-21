# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import pandas as pd
import pickle
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from tmtoolkit.preprocess import TMPreproc
from tmtoolkit.lda_utils import common
from tmtoolkit.lda_utils.common import results_by_parameter
from tmtoolkit.lda_utils.visualize import plot_eval_results

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

#from sqlite import sqlite
from textextraction.extract_frompdf import extract_text


def save_obj(obj):
    with open('pickck.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def train_model():
    import os.path
    from tmtoolkit.lda_utils import tm_lda, tm_gensim, tm_sklearn, visualize
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    import pickle

    picklefile = 'test.pickle'

    if True:#not os.path.isfile(picklefile):
        # load "(text) files
        # corpus = Corpus()
        # corpus.add_files(files=files, encoding='utf-8')
        ini = 0
        corpus = {}
        for file in files:
            ini += 1
            corpus['doc' + str(ini)] = extract_text(file).replace("-\n","")

        # initialize
        preproc = TMPreproc(corpus, language='german')

        # run the preprocessing pipeline: tokenize, POS tag, lemmatize, transform to
        # lowercase and then clean the tokens (i.e. remove stopwords)
        preproc.tokenize().pos_tag().lemmatize().tokens_to_lowercase().clean_tokens() #
        print(preproc.tokens)
        pos_tags = preproc.tokens_with_pos_tags
        save_obj(pos_tags)
        print("##################### PosTags")
        print(pos_tags)

        # generate sparse DTM and print it as a data table
        doc_labels, vocab, dtm = preproc.get_dtm()
        # Test set from Reuters
        # import lda
        # doc_labels = lda.datasets.load_reuters_titles()
        # vocab = lda.datasets.load_reuters_vocab()
        # dtm = lda.datasets.load_reuters()

        print(pd.DataFrame(dtm.todense(), columns=vocab, index=doc_labels))


        ####  evaluate topic models with different parameters
        const_params = dict(n_iter=100, random_state=1)  # low number of iter. just for showing how it works here
        varying_params = [dict(n_topics=k, alpha=1.0/k) for k in range(10, 251, 10)]  # beta=0.01 ??

        # more iterations and more parameter
        #const_params = dict(n_iter=1500, random_state=1, refresh=10)
        #ks = list(range(10, 160, 5)) + list(range(160, 300, 10)) + [300, 325, 350, 375, 400]
        #varying_params = [dict(n_topics=k, alpha=1.0/k) for k in ks]

        # this will evaluate 25 models (with n_topics = 10, 20, .. 250) in parallel
        models = tm_lda.evaluate_topic_models(dtm, varying_params, const_params,
                                              return_models=True)
        #### plot the results
        results_by_n_topics = results_by_parameter(models, 'n_topics')
        plot_eval_results(results_by_n_topics)
        plt.show()

        # the peak seems to be around n_topics == 140

        best_model = dict(results_by_n_topics)[140]['model']
        common.save_ldamodel_to_pickle(picklefile, best_model, vocab, doc_labels, dtm=dtm)


def get_entities(pretoken_path: str, doc_id: str):
    pretoken = load_obj(pretoken_path)  # "pickck.pkl"
    pos_ne = set([t[0] for t in pretoken[doc_id] if t[1]=='NE'])
    return pos_ne


def get_noms(pretoken_path: str, doc_id: str):
    pretoken = load_obj(pretoken_path)  # "pickck.pkl"
    pos_nn = set([t[0] for t in pretoken[doc_id] if t[1]=='NN'])
    return pos_nn


def get_topics(model_path: str, pretoken_path: str, doc_id: str):
    load = common.load_ldamodel_from_pickle(model_path)  # 'test.pickle'
    best_model = load['model']
    vocab = load['vocab']
    doc_labels = load['doc_labels']
    dtm = load['dtm']

    # common.print_ldamodel_topic_words(best_model.topic_word_, vocab)
    # common.print_ldamodel_topic_words(best_model.topic_word_, vocab)
    topic_words = common.ldamodel_top_topic_words(best_model.topic_word_, vocab)
    doc_topics = common.ldamodel_top_doc_topics(best_model.doc_topic_, doc_labels)
    data = doc_topics.loc[doc_id].tolist()
    data = list(map(lambda i: i.split(" (")[0], data))
    topics = list(map(lambda i: i.split(" (")[0], data))
    g = []
    for topic in topics:
        m = topic_words.loc[topic].tolist()
        m = list(map(lambda i: i.split(" (")[0], m))
        g += m
    g = list(set(g) & set(get_noms(pretoken_path, doc_id)))
    return(g)


def create_viz():
    #topic_clouds = visualize.generate_wordclouds_for_topic_words(best_model.topic_word_,
    #                                                             vocab,
    #                                                             top_n=20,
    #                                                             width=400,
    #                                                             height=300)
    #print(topic_clouds.keys())
    #topic_clouds['topic_1'].save('words.png')
    pass


def get_summary(text: str, lang: str, count: 5):
    text = text.replace("-\n", "")
    parser = PlaintextParser.from_string(string=text, tokenizer=Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    return list(summarizer(parser.document, SENTENCES_COUNT))


if __name__ == '__main__':
    LANGUAGE = "german"
    SENTENCES_COUNT = 5
    files = ['../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']

    # train_model()
    print(get_topics("test.pickle", "pickck.pkl", doc_id="doc1"))
    print(get_entities("pickck.pkl", doc_id="doc1"))
    text = extract_text(files[0])
    print(get_summary(text=text, lang=LANGUAGE, count=SENTENCES_COUNT))

