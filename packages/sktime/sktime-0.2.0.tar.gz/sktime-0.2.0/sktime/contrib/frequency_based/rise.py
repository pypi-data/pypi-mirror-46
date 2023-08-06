import numpy as np
import pandas as pd
import math
from numpy import random
from copy import deepcopy
from sklearn.ensemble.forest import ForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.multiclass import class_distribution


class RandomIntervalSpectralForest(ForestClassifier):
    __author__ = "Tony Bagnall"

    """Random Interval Spectral Forest (RISE).

    Random Interval Spectral Forest: stripped down implementation of RISE from Lines 2018:
    @article
    {lines17hive-cote,
     author = {J. Lines, S. Taylor and A. Bagnall},
              title = {Time Series Classification with HIVE-COTE: The Hierarchical Vote Collective of Transformation-Based Ensembles},
    journal = {ACM Transactions on Knowledge and Data Engineering},
    volume = {12},
    number= {5},
    year = {2018}
    
    Overview: Input n series length m
    for each tree
        sample a random intervals
        take the ACF and PS over this interval, and concatenate features
        build tree on new features
    ensemble the trees through averaging probabilities.
    Need to have a minimum interval for each tree
    This is from the python github. 
    For the Java version, see
    https://github.com/TonyBagnall/uea-tsc/blob/master/src/main/java/timeseriesweka/classifiers/RISE.java
    


    Parameters
    ----------
    n_trees         : ensemble size, integer, optional (default = 200)
    random_state    : seed for random, integer, optional (default to no seed)
    dim_to_use      : the column of the panda passed to use, optional (default = 0)
    min_interval    : minimum width of an interval, optional (default = 16)
    acf_lag         : maximum number of autocorellation terms to use (default =100)
    acf_min_values : never use fewer than this number of terms to fnd a correlation (default =4)
    Attributes
    ----------
    num_classes    : extracted from the data
    num_atts       : extracted from the data
    classifiers    : array of DecisionTree classifiers
    intervals      : stores indexes of the start and end points for all classifiers
    dim_to_use     : the column of the panda passed to use (can be passed a multidimensional problem, but will only use one)

    
    """

    def __init__(self,
                 num_trees=500,
                 random_state=None,
                 dim_to_use=0,
                 min_interval=16,
                 acf_lag=100,
                 acf_min_values=4
                 ):
        super(RandomIntervalSpectralForest, self).__init__(
            base_estimator=DecisionTreeClassifier(),
            n_estimators=num_trees)
        self.num_trees=num_trees
        self.random_state = random_state
        random.seed(random_state)
        self.dim_to_use = dim_to_use
        self.min_interval=min_interval
        self.acf_lag=acf_lag
        self.acf_min_values=acf_min_values
        # These are all set in fit
        self.num_classes = 0
        self.series_length = 0
        self.classifiers = []
        self.intervals=[]
        self.lags=[]
        self.classes_ = []

        # For the multivariate case treating this as a univariate classifier
        self.dim_to_use = dim_to_use

    def fit(self, X, y, sample_weight=None):
        """Build a forest of trees from the training set (X, y) using random intervals and summary measures.
        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samps, num_atts]
            The training input samples.  If a Pandas data frame is passed, the column _dim_to_use is extracted
        y : array-like, shape = [n_samples] or [n_samples, n_outputs]
            The class labels.

        Returns
        -------
        self : object
         """

        if isinstance(X, pd.DataFrame):
            if isinstance(X.iloc[0,self.dim_to_use], pd.Series):
                X = np.asarray([a.values for a in X.iloc[:,0]])
            else:
                raise TypeError("Input should either be a 2d numpy array, or a pandas dataframe containing Series objects")
        n_samps, self.series_length = X.shape

        self.num_classes = np.unique(y).shape[0]
        self.classes_ = class_distribution(np.asarray(y).reshape(-1, 1))[0][0]
        self.intervals=np.zeros((self.num_trees, 2), dtype=int)
        self.intervals[0][0] = 0
        self.intervals[0][1] = self.series_length
        for i in range(1, self.num_trees):
            self.intervals[i][0]=random.randint(self.series_length - self.min_interval)
            self.intervals[i][1]=random.randint(self.intervals[i][0] + self.min_interval, self.series_length)
        # Check lag against global properties
        if self.acf_lag > self.series_length-self.acf_min_values:
            self.acf_lag = self.series_length - self.acf_min_values
        if self.acf_lag < 0:
            self.acf_lag = 1
        self.lags=np.zeros(self.num_trees, dtype=int)
        for i in range(0, self.num_trees):
            temp_lag=self.acf_lag
            if temp_lag > self.intervals[i][1]-self.intervals[i][0]-self.acf_min_values:
                temp_lag = self.intervals[i][1] - self.intervals[i][0] - self.acf_min_values
            if temp_lag < 0:
                temp_lag = 1
            self.lags[i] = int(temp_lag)
            acf_x = np.empty(shape=(n_samps,self.lags[i]))
            ps_len = (self.intervals[i][1] - self.intervals[i][0]) / 2
            ps_x = np.empty(shape=(n_samps,int(ps_len)))
            for j in range(0, n_samps):
                acf_x[j] = acf(X[j,self.intervals[i][0]:self.intervals[i][1]], temp_lag)
                ps_x[j] = ps(X[j, self.intervals[i][0]:self.intervals[i][1]])
            transformed_x = np.concatenate((acf_x,ps_x),axis=1)
#            transformed_x=acf_x
            tree = deepcopy(self.base_estimator)
            tree.fit(transformed_x, y)
            self.classifiers.append(tree)
        return self

    def predict(self, X):
        """
        Find predictions for all cases in X. Built on top of predict_proba
        Parameters
        ----------
        X : The training input samples.  array-like or sparse matrix of shape = [n_samps, num_atts] or a data frame.
        If a Pandas data frame is passed, the column _dim_to_use is extracted

        Returns
        -------
        output : 1D array of predictions,
        """

        probs=self.predict_proba(X)
        return [self.classes_[np.argmax(prob)] for prob in probs]

    def predict_proba(self, X):
        """
        Find probability estimates for each class for all cases in X.
        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samps, num_atts]
            The training input samples.  If a Pandas data frame is passed, the column _dim_to_use is extracted

        Local variables
        ----------
        n_samps     : number of cases to classify
        num_atts    : number of attributes in X, must match _num_atts determined in fit

        Returns
        -------
        output : 2D array of probabilities,
        """
        if isinstance(X, pd.DataFrame):
            if isinstance(X.iloc[0,self.dim_to_use],pd.Series):
                X = np.asarray([a.values for a in X.iloc[:,0]])
            else:
                raise TypeError("Input should either be a 2d numpy array, or a pandas dataframe containing Series objects")
        rows,cols=X.shape
        #HERE Do transform againnum_att
        n_samps, num_atts = X.shape
        if num_atts != self.series_length:
            raise TypeError(" ERROR number of attributes in the train does not match that in the test data")
        sums = np.zeros((X.shape[0],self.num_classes), dtype=np.float64)

        for i in range(0, self.num_trees):
            acf_x = np.empty(shape=(n_samps, self.lags[i]))
            ps_len=(self.intervals[i][1] - self.intervals[i][0]) / 2
            ps_x = np.empty(shape=(n_samps,int(ps_len)))
            for j in range(0, n_samps):
                acf_x[j] = acf(X[j, self.intervals[i][0]:self.intervals[i][1]], self.lags[i])
                ps_x[j] = ps(X[j, self.intervals[i][0]:self.intervals[i][1]])
            transformed_x=np.concatenate((acf_x,ps_x),axis=1)
            sums += self.classifiers[i].predict_proba(transformed_x)

        output = sums / (np.ones(self.num_classes) * self.n_estimators)
        return output

def acf(x, max_lag):
    """ autocorrelation function transform, currently calculated using standard stats method.
    We could use inverse of power spectrum, especially given we already have found it, worth testing for speed and correctness
    HOWEVER, for long series, it may not give much benefit, as we do not use that many ACF terms

    Parameters
    ----------
    x : a 1D array
    max_lag: number of ACF terms to find

    Return
    ----------
    an array of length max_lag

    """
    y = np.zeros(max_lag)
    length=len(x)
    for lag in range(1, max_lag + 1):
# Could just do it ourselves ... TO TEST
        s1=np.sum(x[:-lag])
        ss1=np.sum(np.square(x[:-lag]))
        s2=np.sum(x[lag:])
        ss2=np.sum(np.square(x[lag:]))
        s1=s1/(length-lag)
        s2 = s2 / (length - lag)
        y[lag-1] = np.sum((x[:-lag]-s1)*(x[lag:]-s2))
        y[lag - 1] = y[lag - 1]/ (length - lag)
        v1 = ss1/(length - lag)-s1*s1
        v2 = ss2/(length-lag)-s2*s2
#        print(v1)
#        print(v2)
        if v1 <= 0.000000001 and v2 <= 0.000000001: # Both zero variance, so must be 100% correlated
            y[lag - 1]=1
        elif v1 <= 0.000000001 or v2 <= 0.000000001: # One zero variance the other not
            y[lag - 1] = 0
        else:
            y[lag - 1] = y[lag - 1]/(math.sqrt(v1)*math.sqrt(v2))
#        y[lag - 1] = np.corrcoef(x[lag:], x[:-lag])[0][1]
#        if np.isnan(y[lag - 1]) or np.isinf(y[lag-1]):
#            y[lag-1]=0
    return np.array(y)



def matrix_acf(x, num_cases, max_lag):
    """ autocorrelation function transform, currently calculated using standard stats method.
    We could use inverse of power spectrum, especially given we already have found it, worth testing for speed and correctness
    HOWEVER, for long series, it may not give much benefit, as we do not use that many ACF terms

    Parameters
    ----------
    x : a matrix of num_cases,
    max_lag: number of ACF terms to find

    Return
    ----------
    an matrix of length max_lag

    """
    y = np.empty(shape=(num_cases,max_lag))
    for lag in range(1, max_lag + 1):
        # Could just do it ourselves ... TO TEST
        #            s1=np.sum(x[:-lag])/x.shape()[0]
        #            ss1=s1*s1
        #            s2=np.sum(x[lag:])
        #            ss2=s2*s2
        #
        y[lag - 1] = np.corrcoef(x[:,lag:], x[:,-lag])[0][1]
        if np.isnan(y[lag - 1]) or np.isinf(y[lag-1]):
            y[lag-1]=0
    return y



def ps(x):
    """ power spectrum transform, currently calculated using np function.
    It would be worth looking at ff implementation, see difference in speed to java
    Parameters
    ----------
    x : an array

    Return
    ----------
    an array of length x.length/2
    """
    fft=np.fft.fft(x)
    fft=fft.real*fft.real+fft.imag*fft.imag
    fft=fft[:int(len(x)/2)]
    return np.array(fft)

if __name__ == "__main__":
    x = [1,2,2,3,3,1,3,4,6,6,7,8]
    x = [1,1,1,1,1,1,1,1,1,1,1,1]
    max_lag = 2
    y = np.zeros(max_lag)
    length=len(x)
#Built in version complains when zero variance
    for lag in range(1, max_lag + 1):
        y[lag - 1] = np.corrcoef(x[lag:], x[:-lag])[0][1]
        if np.isnan(y[lag - 1]) or np.isinf(y[lag - 1]):
            y[lag - 1] = 0
    print(y)
    a=acf(x,2)
    print(a)