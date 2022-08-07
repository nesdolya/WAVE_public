## Filename: waveHMM.py
## Program Description: Custom subclass that inhertis the hmmlearn BaseHMM class to utilize custom emission probability density functions
## Author: Andrea Nesdoly 
## Created: November, 2019
## See hmmlearn documentation for more information: https://hmmlearn.readthedocs.io/en/latest/
## Code:

import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.utils import check_random_state
from hmmlearn.base import _BaseHMM
from hmmlearn.utils import normalize

#include _BaseHMM in brackets to inherit it's methods
class waveHMM(_BaseHMM):
  
    #_init for waveHMM
    def _init(self, X, lengths=None):
        """Initializes model parameters prior to fitting.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix of individual samples.
        lengths : array-like of integers, shape (n_sequences, )
            Lengths of the individual sequences in ``X``. The sum of
            these should be ``n_samples``.
        """
        
        #we want to allow X to be type float but non-negative    
        self._check_non_negative(X)
        
        #call on the _BaseHMM() _init which initializes the start and transmission probs
        super()._init(X, lengths=lengths)
        #self.n_features = 1
        
        self.random_state = check_random_state(self.random_state)

        #initialize emission probabilities
        #taken from multinomial _init which uses discrete variables, so has an array of (n_components,n_features)
        # will be array (n_components,1) --> [dgammafit,geninvgaussfit]
        if 'e' in self.init_params:
            self.emissionprob_ = self.random_state.rand(self.n_components, self.n_features)
            #print('Init emission probs before:',self.emissionprob_)
            normalize(self.emissionprob_, axis=1)
            #print('Init emission probs after:',self.emissionprob_)

    #for waveHMM
    def _check(self):
        """Validates model parameters prior to fitting.
        Raises
        ------
        ValueError
            If the start, transmission, or emission probabilites are incorrect (i.e. start probabilities do not sum to 1),
            or are not the correct shape.
        """
        
        #_BaseHMM _check looks at the start prob and transmission probs for validity
        super()._check()
        
        #mulitnomial check for the correct array shape (n_components, n_features)
        #check that the emissions probs are at least a 2d array
        self.emissionprob_ = np.atleast_2d(self.emissionprob_)

        #set the attribute size (should be 1)
        #multinomial:: self.emissionprob_.shape[1] won't work if passing best fit (tuple parameters are different sizes)
        n_features = getattr(self, "n_features", 1)
        #print(n_features)
        
        #raise error if the shape of the emission probabilities is incorrect array 
        #    should be (n_components,1) --> [dgammafit,geninvgaussfit]
        if self.emissionprob_.shape != (self.n_components, n_features):
            raise ValueError(
                "emissionprob_ must have shape (n_components, n_features)")
        else:
            self.n_features = n_features
    
    #for waveHMM
    def _compute_log_likelihood(self, X):
        """Computes per-component log probability under the model.
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Feature matrix of individual samples.
        Returns
        -------
        logprob : array, shape (n_samples, n_components)
            Log probability of each sample in ``X`` for each of the
            model states.
        """
        
        #return array (X.length,2) where 1st row is wv=0(dgamma) and 2nd row is wv=1(geninvgauss)
        #these functions are passed in, but are essentially hard coded
        dg,gigaus = self.emissionprob_
        #print('log likelihood emissions prob:',self.emissionprob_)
        
        d=dg[0]
        g=gigaus[0]
        
        #print(d)
        #print(gigaus)
        
        #the log of the pdf is the log likelihood for each observation passed in X
        non = stats.dgamma.logpdf(X, *d)
        wv = stats.geninvgauss.logpdf(X, *g)
        
        return np.append(non,wv,axis=1)
  

    #for waveHMM
    def _generate_sample_from_state(self, state, random_state=None):
        """Generates a random sample from a given component.
        Parameters
        ----------
        state : int
            Index of the component to condition on.
        random_state: RandomState or an int seed
            A random number generator instance. If ``None``, the object's
            ``random_state`` is used.
        Returns
        -------
        X : array, shape (n_features, )
            A random sample from the emission distribution corresponding
            to a given component.
        """
        
        dg,gigaus = self.emissionprob_
        
        random_state = check_random_state(random_state)
        
        #looked at using cdf function as mutinomial did, but this returned discrete values where we want continuous 
        #    observation samples.
        #round values to 1 decimal place as they are in SOG for CCG data --> other AIS data goes to at least 3 decimal places
        if state ==0:
            #cdf = stats.dgamma.cdf(lns, *dg)
            return np.round(stats.dgamma.rvs(*dg,random_state=random_state),1)
        if state ==1:
            #cdf = stats.geninvgauss.cdf(lns, *gigaus)
            return np.round(stats.geninvgauss.rvs(*gigaus,random_state=random_state),1)
        
        #there are only two possible states, so raise error if stat outside of the set {1,2}
        else:
            raise ValueError("State must be either 0 or 1")

    #for waveHMM
    #the initial creation of this model will not be fitting the emission parameters using EM alg, so maybe unnessecary?
    def _initialize_sufficient_statistics(self):
        """Initializes sufficient statistics required for M-step.
        The method is *pure*, meaning that it doesn't change the state of
        the instance.  For extensibility computed statistics are stored
        in a dictionary.
        Returns
        -------
        The super() initializes the below parameters
        nobs : int
            Number of samples in the data.
        start : array, shape (n_components, )
            An array where the i-th element corresponds to the posterior
            probability of the first sample being generated by the i-th
            state.
        trans : array, shape (n_components, n_components)
            An array where the (i, j)-th element corresponds to the
            posterior probability of transitioning between the i-th to j-th
            states.
        
        The subclass initializes the emission probabilities by adding an item to the dictionary
        obs  : array, shape (n_components, n_features)
            An array where the (i, j)-th element corresponds to the parameters 
            required to reproduce the emissions probability density curve for
            the i-th state and j-th feature (in this case a single SOG feature).
        """
        #intialization of the number of samples, and the start and transmission probabilities
        stats = super()._initialize_sufficient_statistics()
        
        #add initialization of observation stats for fitting
        stats['obs'] = np.zeros((self.n_components, self.n_features))
        return stats
    
    #from multinomial
    def _do_mstep(self, stats):
        """Performs the M-step of EM algorithm.
        Parameters
        ----------
        stats : dict
            Sufficient statistics updated from all available samples.
        """
        super()._do_mstep(stats)
        if 'e' in self.params:
            self.emissionprob_ = (
                stats['obs'] / stats['obs'].sum(axis=1, keepdims=True))

    #for waveHMM
    def _check_non_negative(self,X):
        """Supplements _check() for non-negative SOG values
        There should be none in the clean CCG data
        """
        #check that observations are not negative
        if X.min() < 0:
            raise ValueError("Symbols should be non-negative")
            

"""
Example code to run the HMM with custom emissions probabilities
"""

## Ingest data as pandas dataframe
data = pd.read_csv('path/to/data.csv')

## Initial, transition, and emission probabilities were previously derived through statistical analysis

# Initial Probabilities
pi_sample = #tranisition matrix previously developed

# Transition Probabilities
alpha = #tranisition matrix previously developed

# Emission Probability functions - Custom PDF using the desired variable (e.g. SOG)
# double gamma & generalized inverse Gaussian distribution functions
x = np.array(data.SOG)
dgammafit = stats.dgamma.fit(x)
geninvgaussfit = stats.geninvgauss.fit(x)

# Sort data based on timestamp and reshape for model use
data = data.sort_values('timestamp')
X = data.SOG.values.reshape(-1,1)

## Run HMM
#Create HMM object: using the known start, transission, and emission probabilities 
#       possible parameterization includes (n_components=1, startprob_prior=1.0, transmat_prior=1.0, algorithm='viterbi', 
#                        random_state=None, n_iter=10, tol=0.01, verbose=False, 
#                        params='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 
#                        init_params='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
#   only setting the states, start probs, transmission probs, emission probs, decode algorithgm, and verbose
#       params and init_params are not set in this case because no training required

model_waveHMM = waveHMM(n_components=2,algorithm='viterbi',verbose=True)

# Assign custom probabilities
model_waveHMM.startprob_ = pi_sample
model_waveHMM.transmat_ = alpha
model_waveHMM.emissionprob_ = np.array([dgammafit,geninvgaussfit]).reshape(2,1)
model_waveHMM.startprob_

#predict/decode without using the lengths of the trips
ccg_waveHMM_decode = model_waveHMM.decode(X)
ccg_waveHMM_predict = model_waveHMM.predict(X)

#predict/decode using the lengths of the trips if known
#ccg_waveHMM_decode = model_waveHMM.decode(X,lengths=lengths)
#ccg_waveHMM_predict = model_waveHMM.predict(X,lengths=lengths)
