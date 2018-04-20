from tmtoolkit.preprocess import TMPreproc
from tmtoolkit.corpus import Corpus
import pandas as pd
import tmtoolkit

def main():
    # load "(text) files
    corpus = Corpus()
    corpus.add_files(files=['../exampleData/Faust_I.txt'], encoding='utf-8')

    # initialize
    preproc = TMPreproc(corpus, language='german')

    # run the preprocessing pipeline: tokenize, POS tag, lemmatize, transform to
    # lowercase and then clean the tokens (i.e. remove stopwords)
    preproc.tokenize().pos_tag().lemmatize().tokens_to_lowercase().clean_tokens()

    print(preproc.tokens)

    print(preproc.tokens_with_pos_tags)

    # generate sparse DTM and print it as a data table
    doc_labels, vocab, dtm = preproc.get_dtm()

    print(pd.DataFrame(dtm.todense(), columns=vocab, index=doc_labels))


    ##########
    from tmtoolkit.lda_utils import tm_lda
    import lda  # for the Reuters dataset

    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    doc_labels = lda.datasets.load_reuters_titles()
    vocab = lda.datasets.load_reuters_vocab()
    dtm = lda.datasets.load_reuters()

    # evaluate topic models with different parameters
    const_params = dict(n_iter=100, random_state=1)  # low number of iter. just for showing how it works here
    varying_params = [dict(n_topics=k, alpha=1.0/k) for k in range(10, 251, 10)]

    # this will evaluate 25 models (with n_topics = 10, 20, .. 250) in parallel
    models = tm_lda.evaluate_topic_models(dtm, varying_params, const_params,
                                          return_models=True)

    # plot the results
    # note that since we used a low number of iterations, the plot looks quite "unstable"
    # for the given metrics.
    from tmtoolkit.lda_utils.common import results_by_parameter
    from tmtoolkit.lda_utils.visualize import plot_eval_results

    results_by_n_topics = results_by_parameter(models, 'n_topics')
    plot_eval_results(results_by_n_topics)
    plt.show()

    # the peak seems to be around n_topics == 140
    from tmtoolkit.lda_utils.common import print_ldamodel_topic_words, print_ldamodel_doc_topics

    best_model = dict(results_by_n_topics)[140]['model']
    print_ldamodel_topic_words(best_model.topic_word_, vocab)
    print_ldamodel_doc_topics(best_model.doc_topic_, doc_labels)


if __name__ == '__main__':
    main()

