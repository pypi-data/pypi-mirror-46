import scipy.sparse as sp
import numpy as np
from sklearn.utils.validation import check_array, FLOAT_DTYPES
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, _document_frequency

class MyTfidfTransformer(TfidfTransformer):
    def __init__(self,
                 norm='l2',
                 use_idf=True,
                 smooth_idf=True,
                 sublinear_tf=False):
        self.norm = norm
        self.use_idf = use_idf
        self.smooth_idf = smooth_idf
        self.sublinear_tf = sublinear_tf

    def fit(self, X, y=None):
        """Learn the idf vector (global term weights)
        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
            a matrix of term/token counts
        """
        X = check_array(X, accept_sparse=('csr', 'csc'))
        if not sp.issparse(X):
            X = sp.csr_matrix(X)
        dtype = X.dtype if X.dtype in FLOAT_DTYPES else np.float64

        if self.use_idf:
            n_samples, n_features = X.shape
            df = _document_frequency(X).astype(dtype)

            # perform idf smoothing if required
            df += int(self.smooth_idf)
            n_samples += int(self.smooth_idf)

            # log+1 instead of log makes sure terms with zero idf don't get
            # suppressed entirely.
            # idf = np.log(n_samples / df) + 1
            idf = df
            self._idf_diag = sp.diags(
                idf,
                offsets=0,
                shape=(n_features, n_features),
                format='csr',
                dtype=dtype)
        return self


class MyTfidfVectorizer(TfidfVectorizer):
    def __init__(self,
                 input='content',
                 encoding='utf-8',
                 decode_error='strict',
                 strip_accents=None,
                 lowercase=True,
                 preprocessor=None,
                 tokenizer=None,
                 analyzer='word',
                 stop_words=None,
                 token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1),
                 max_df=1.0,
                 min_df=1,
                 max_features=None,
                 vocabulary=None,
                 binary=False,
                 dtype=np.float64,
                 norm='l2',
                 use_idf=True,
                 smooth_idf=True,
                 sublinear_tf=False):

        super(TfidfVectorizer, self).__init__(
            input=input,
            encoding=encoding,
            decode_error=decode_error,
            strip_accents=strip_accents,
            lowercase=lowercase,
            preprocessor=preprocessor,
            tokenizer=tokenizer,
            analyzer=analyzer,
            stop_words=stop_words,
            token_pattern=token_pattern,
            ngram_range=ngram_range,
            max_df=max_df,
            min_df=min_df,
            max_features=max_features,
            vocabulary=vocabulary,
            binary=binary,
            dtype=dtype)

        self._tfidf = MyTfidfTransformer(
            norm=norm,
            use_idf=use_idf,
            smooth_idf=smooth_idf,
            sublinear_tf=sublinear_tf)

    # Broadcast the TF-IDF parameters to the underlying transformer instance
    # for easy grid search and repr

    def fit_transform(self, raw_documents, y=None):
        """Learn vocabulary and idf, return term-document matrix.
        This is equivalent to fit followed by transform, but more efficiently
        implemented.
        Parameters
        ----------
        raw_documents : iterable
            an iterable which yields either str, unicode or file objects
        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Tf-idf-weighted document-term matrix.
        """
        self._check_params()
        X = super(TfidfVectorizer, self).fit_transform(raw_documents)
        self._tfidf.fit(X)
        # X is already a transformed view of raw_documents so
        # we set copy to False
        return self._tfidf.transform(X, copy=False)