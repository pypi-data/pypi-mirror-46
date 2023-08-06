import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from vgram import loadStreamVGram, StreamVGram

from data_reader import get_20ng


def learn_svm_on_vgram(X_tr, X_te, y_tr, y_te):
    data = X_tr + X_te

    stream_vgram = StreamVGram(15000)
    for i in range(15):
        for s in data:
            stream_vgram.accept(s)
    stream_vgram.update()
    vtrain = [stream_vgram.parse(s) for s in X_tr]
    vtest = [stream_vgram.parse(s) for s in X_te]

    pipeline = Pipeline([
        ("vect", CountVectorizer()),
        ('tfidf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100))
    ])
    pipeline.fit(vtrain, y_tr)

    print("train accuracy: ", np.mean(pipeline.predict(vtrain) == y_tr))
    print("test accuracy: ", np.mean(pipeline.predict(vtest) == y_te))


# Then we use small dictionary, less data and less iteration only for faster fitting.
# This is bad parameters for real-world solution, see learn_svm_on_vgram for good parameters example


def save_learned_vgram(X_tr, X_te, path):
    data = X_tr + X_te
    data = data[:1000]
    stream_vgram = StreamVGram(500)
    for s in data:
        stream_vgram.accept(s)
    stream_vgram.update()
    stream_vgram.save(path)


def load_learned_vgram_for_svm(X_tr, X_te, y_tr, y_te, path):
    stream_vgram = loadStreamVGram(path)
    vtrain = [stream_vgram.parse(s) for s in X_tr]
    vtest = [stream_vgram.parse(s) for s in X_te]
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer()),
        ('tfidf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100))
    ])
    pipeline.fit(vtrain, y_tr)
    print("train accuracy: ", np.mean(pipeline.predict(vtrain) == y_tr))
    print("test accuracy: ", np.mean(pipeline.predict(vtest) == y_te))


def show_learned_dictionary(path):
    vgram = loadStreamVGram(path)
    print(vgram.alphabet()[:10])


if __name__ == "__main__":
    path = "vgram_dict.json"
    X_tr, X_te, y_tr, y_te = get_20ng()
    save_learned_vgram(X_tr, X_te, path)
    show_learned_dictionary(path)
