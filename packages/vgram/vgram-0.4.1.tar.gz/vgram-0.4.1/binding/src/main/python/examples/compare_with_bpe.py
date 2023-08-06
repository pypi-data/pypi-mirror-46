import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import sentencepiece as spm
from vgram import loadVGram, VGram
from .data_reader import get_20ng, get_imdb


def svm_on_vgram(X_tr, X_te, y_tr, y_te, size=15000, iters=10, path=None):
    if path is None:
        vgram = VGram(size, iters).fit(X_tr + X_te)
    else:
        vgram = loadVGram(path)
    pipeline = Pipeline([
        ("vgb", vgram),
        ("vectorizer", CountVectorizer()),
        ('tfidf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100))
    ])
    pipeline.fit(X_tr, y_tr)
    print(f"train accuracy: {np.mean(pipeline.predict(X_tr) == y_tr)}")
    print(f"test accuracy: {np.mean(pipeline.predict(X_te) == y_te)}")


def save_learned_bpe(X_tr, X_te, size, path):
    data = X_tr + X_te
    with open(path) as f:
        for s in data:
            f.write(s + "\n")
    spm.SentencePieceTrainer.Train(f'--input={path} --model_prefix=m --vocab_size={size}')


if __name__ == "__main__":
    path = "vgram_dict_20ng_15k_10.json"
    sp_path = "sp_model_20ng_15k_10.json"
    X_tr, X_te, y_tr, y_te = get_20ng()
    # X_tr, X_te, y_tr, y_te = get_imdb()
    size = 15000
    iters = 3
    # svm_on_vgram(X_tr, X_te, y_tr, y_te, size, iters, path=None)
    save_learned_bpe(X_tr, X_te, size, sp_path)
