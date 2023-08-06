from ..utils.validation import check_equal_index
from ..utils.transformations import tabularize
from .series_to_series import RandomIntervalSegmenter
from sklearn.utils.validation import check_is_fitted
import numpy as np
import pandas as pd

__all__ = ['RandomIntervalFeatureExtractor']


class RandomIntervalFeatureExtractor(RandomIntervalSegmenter):
    """
    Transformer that segments time-series into random intervals
    and subsequently extracts series-to-primitives features from each interval.

    n_intervals: str{'sqrt', 'log', 'random'}, int or float, optional (default='sqrt')
        Number of random intervals to generate, where m is length of time series:
        - If "log", log of m is used.
        - If "sqrt", sqrt of m is used.
        - If "random", random number of intervals is generated.
        - If int, n_intervals intervals are generated.
        - If float, int(n_intervals * m) is used with n_intervals giving the fraction of intervals of the
        time series length.

        For all arguments relative to the length of the time series, the generated number of intervals is
        always at least 1.

    features: list of functions, optional (default=None)
        Applies each function to random intervals to extract features.
        If None, only the mean is extracted.

    random_state: : int, RandomState instance, optional (default=None)
        - If int, random_state is the seed used by the random number generator;
        - If RandomState instance, random_state is the random number generator;
        - If None, the random number generator is the RandomState instance used
        by `np.random`.

    check_input: bool, optional (default=True)
        When set to ``True``, inputs will be validated, otherwise inputs are assumed to be valid
        and no checks are performed. Use with caution.
    """

    def __init__(self, n_intervals='sqrt', min_length=None, features=None, random_state=None, check_input=True):
        super(RandomIntervalFeatureExtractor, self).__init__(
            n_intervals=n_intervals,
            min_length=min_length,
            random_state=random_state,
            check_input=check_input
        )

        # Check input of feature calculators, i.e list of functions to be applied to time-series
        if features is None:
            self.features = [np.mean]
        elif isinstance(features, list) and all([callable(func) for func in features]):
            self.features = features
        else:
            raise ValueError('Features must be list containing only functions (callables) to be '
                             'applied to the data columns')

    def transform(self, X, y=None):
        """
        Transform X, segments time-series in each column into random intervals using interval indices generated
        during `fit` and extracts features from each interval.

        Parameters
        ----------
        X : nested pandas.DataFrame of shape [n_samples, n_features]
            Nested dataframe with time-series in cells.

        Returns
        -------
        Xt : pandas.DataFrame
          Transformed pandas DataFrame with same number of rows and one column for each generated interval.
        """

        # Check is fit had been called
        check_is_fitted(self, 'intervals_')

        # check inputs
        if self.check_input:
            # Check that the input is of the same shape as the one passed
            # during fit.
            if X.shape[1] != self.input_shape_[1]:
                raise ValueError('Number of columns of input is different from what was seen'
                                 'in `fit`')
            # Input validation
            if not all([np.array_equal(fit_idx, trans_idx) for trans_idx, fit_idx in zip(check_equal_index(X),
                                                                                         self.input_indexes_)]):
                raise ValueError('Indexes of input time-series are different from what was seen in `fit`')

        n_rows, n_cols = X.shape
        n_features = len(self.features)
        n_cols_intervals = sum([intervals.shape[0] for intervals in self.intervals_])

        # Compute features on intervals.
        Xt = np.zeros((n_rows, n_features * n_cols_intervals))  # Allocate output array for transformed data
        self.columns_ = []
        i = 0
        for c, (colname, col) in enumerate(X.items()):
            # Tabularize each column assuming series have equal indexes in any given column.
            # TODO generalise to non-equal-index cases
            arr = tabularize(col, return_array=True)
            for func in self.features:
                # TODO generalise to series-to-series functions and function kwargs
                for start, end in self.intervals_[c]:
                    interval = arr[:, start:end]

                    # Try to use optimised computations over axis if possible, otherwise iterate over rows.
                    try:
                        Xt[:, i] = func(interval, axis=1)
                    except TypeError as e:
                        if str(e) == f"{func.__name__}() got an unexpected keyword argument 'axis'":
                            Xt[:, i] = np.apply_along_axis(func, 1, interval)
                        else:
                            raise
                    i += 1
                    self.columns_.append(f'{colname}_{start}_{end}_{func.__name__}')
        Xt = pd.DataFrame(Xt)
        Xt.columns = self.columns_
        return Xt
