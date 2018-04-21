#
import pandas as pd
import pickle
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from tmtoolkit.preprocess import TMPreproc
from tmtoolkit.lda_utils import common
from tmtoolkit.lda_utils.common import results_by_parameter
from tmtoolkit.lda_utils.visualize import plot_eval_results

from sqlite import sqlite
from textextraction.extract_frompdf import extract_text


def save_obj(obj):
    with open('pickck.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


files = ['../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']


def pre():
    conn, c = sqlite.openconnection('sqlite/example.db')
    for file in files:
        with open(file=file) as f:
            sqlite.insertData(c, file,['',''],f.read().replace('\n', ''), file.rsplit('.',1)[0])
    sqlite.closeConnection(conn)


def main():
    import os.path
    from tmtoolkit.lda_utils import tm_lda, tm_gensim, tm_sklearn, visualize
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    import pickle

    picklefile = 'test.pickle'

    if not os.path.isfile(picklefile):
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
        preproc.tokenize().pos_tag().lemmatize().clean_tokens() # .tokens_to_lowercase()
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


def analysis(model_path: str, pretoken_path: str, doc_id: str):
    load = common.load_ldamodel_from_pickle(model_path)  # 'test.pickle'
    best_model = load['model']
    vocab = load['vocab']
    doc_labels = load['doc_labels']
    dtm = load['dtm']
    pretoken = load_obj(pretoken_path)  # "pickck.pkl"
    print(best_model)

    pos_ne = [t[0] for t in pretoken[doc_id] if t[1]=='NE']
    pos_nn = [t[0] for t in pretoken[doc_id] if t[1]=='NN']

    # common.print_ldamodel_topic_words(best_model.topic_word_, vocab)
    # common.print_ldamodel_topic_words(best_model.topic_word_, vocab)
    topic_words = common.ldamodel_top_topic_words(best_model.topic_word_, vocab)
    doc_topics = common.ldamodel_top_doc_topics(best_model.doc_topic_, doc_labels)
    data = doc_topics.loc[doc_id].tolist()
    data = list(map(lambda i: i.split(" (")[0], data))
    return(data)


def create_viz():
    #topic_clouds = visualize.generate_wordclouds_for_topic_words(best_model.topic_word_,
    #                                                             vocab,
    #                                                             top_n=20,
    #                                                             width=400,
    #                                                             height=300)
    #print(topic_clouds.keys())
    #topic_clouds['topic_1'].save('words.png')
    pass



if __name__ == '__main__':
    print(analysis("test.pickle", "pickck.pkl", doc_id="doc1"))
    #conn, c = sqlite.openconnection('sqlite/example.db')
    #for file in files:
    #    with open(file=file, encoding='utf-8') as f:
    #        sqlite.insertData(c, file,['',''],f.read().replace('\n', ''), file.rsplit('.',1)[0])
    #sqlite.closeConnection(conn)

