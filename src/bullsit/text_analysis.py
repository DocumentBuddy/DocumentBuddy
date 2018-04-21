import numpy as np  # a conventional alias
import sklearn.feature_extraction.text as text

def test():

    vectorizer = text.CountVectorizer(input='filename', stop_words='english', min_df=2) #
    dtm = vectorizer.fit_transform(['../exampleData/Faust_I.txt', '../exampleData/Faust_II.txt']).toarray()
    vocab = np.array(vectorizer.get_feature_names())
    print(dtm.shape)
    print(len(vocab))

    from sklearn import decomposition
    num_topics = 20
    num_top_words = 20
    clf = decomposition.NMF(n_components=num_topics, random_state=1)
    doctopic = clf.fit_transform(dtm)
    topic_words = []
    for topic in clf.components_:
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        topic_words.append([vocab[i] for i in word_idx])
    doctopic = doctopic / np.sum(doctopic, axis=1, keepdims=True)
    novel_names = []
    for fn in filenames:
        basename = os.path.basename(fn)
        name, ext = os.path.splitext(basename)
        name = name.rstrip('0123456789')
        novel_names.append(name)
    # turn this into an array so we can use NumPy functions
    novel_names = np.asarray(novel_names)

    doctopic_orig = doctopic.copy()

    # use method described in preprocessing section
    num_groups = len(set(novel_names))

    doctopic_grouped = np.zeros((num_groups, num_topics))

    for i, name in enumerate(sorted(set(novel_names))):
        doctopic_grouped[i, :] = np.mean(doctopic[novel_names == name, :], axis=0)

    doctopic = doctopic_grouped

    print(doctopic)

    import operator
    x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    sorted_x = sorted(vectorizer.vocabulary_.items(), key=operator.itemgetter(1), reverse=True)

from sklearn.feature_extraction.text import CountVectorizer

with open('../exampleData/Faust_I.txt', 'r', encoding='utf-8') as myfile:
    data=myfile.read().replace('\n', '').split('.')
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(data).todense()
    import operator
    x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    sorted_x = sorted(vectorizer.vocabulary_.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x)