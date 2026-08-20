from sklearn.base import BaseEstimator, TransformerMixin

class MeanTargetEncoderSmoothed(BaseEstimator, TransformerMixin):

    def __init__(self, categorical, smoothing=10.0):

        self.categorical = categorical
        self.smoothing = smoothing

    def fit(self, X, y=None):

        data = X.copy()
        data['target'] = y.values

        self.global_mean_ = data['target'].mean()
        self.encoding_maps_ = {}

        for col in self.categorical:
            stats = data.groupby(col)['target'].agg(['mean', 'count'])

            smoothed = (stats['count'] * stats['mean'] + self.smoothing * self.global_mean_) / (stats['count'] + self.smoothing)
            self.encoding_maps_[col] = smoothed

        return self

    def transform(self, X):

        temp = X.copy()

        for col in self.categorical:
            mapped = temp[col].map(self.encoding_maps_[col])

            mapped = mapped.fillna(self.global_mean_)

            temp[col] = mapped

        return temp

    def fit_transform(self, X, y = None, **fit_params):
        return self.fit(X, y).transform(X)