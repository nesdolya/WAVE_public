# Whale-watchin AIS Vessel movement Evaluation Project Public Repository
By: Andrea Nesdoly (nesdolya@uvic.ca)
SURREAL & CORAL Groups, University of Victoria, Department of Geography

## WAVE Project
The WAVE Project's goals are to understand whale-watching activities using Automatic Identification System (AIS), and to determine the feasibility of utilizing AIS data as a tool for informing whale-watching operations, vessel traffic management, conservation, and policy.

Please visit the WAVE Project website to learn more: https://waveproject.ca/

## Modelling marine vessels engaged in wildlife-viewing behaviour using Automatic Identification Systems (AIS)
Andrea Nesdoly (MSc Thesis Work)

The WAVE Project has afforded an opporuntity to model whale-watching vessel behavior with AIS and classify this behaviour. The MSc student on this project (Andrea Nesdoly/myself) has tested three established classification models to find when the vessels are observing wildlife and when they are not (Phase 1). One of these successful models was then deployed to determine if behavior classification utlizing machine learning is feasible when scaled up to the whole whale-watching vessel fleet surrounding Vancouver Island, Coastal British Columbia (Phase 2).

Publications to come.  
For detailed information on the data preparation, methods development, parameterization, and results of this study visit: Nesdoly, A. (2021). Modelling marine vessels engaged in wildlife-viewing behaviour using Automatic Identification Systems (AIS). [Master Thesis, University of Victoria]. UVicSpace. http://hdl.handle.net/1828/13300

### Scripts
The scripts used in this research were developed using Anaconda and Python 3.8 and 3.9. Established Python libraries that were used for statistical analysis and model development include:
- [scikit-learn](https://scikit-learn.org/stable/)
- [scipy](https://scipy.org/)
- [hmmlearn](https://hmmlearn.readthedocs.io/en/latest/)
- [statsmodels](https://www.statsmodels.org/stable/index.html) 

Research Phase 1: The Hidden Markov Model required a custom subclass [waveHMM.py]() of the hmmlearn API to utilize custom emission probability density functions. This subclass inherts the hmmlearn.base.BaseHMM class methods. The initial, transition, and emission probabilities were derived through statistical analysis before being utilized by the waveHMM subclass. Continuous probability distribution functions were fit the SOG profiles for the wildlife-viewing and non-viewing states, and the optimal probability distribution functions were fitted by minimizing the negative log-likelihood.|

## Table of Scripts and Notebooks
|Name|Description|Collaborators|
|----|-----------|-------------|
|listen_aishub.py| A script developed to listen to the incoming stream of AIS data from AISHub, a crowdsourced data streaming platform. This basic script runs indefinately, storing each days AIS NMEA format data as a text file. Each month is then archived in a .zip folder. This program is currently running on a cloud server using supervisord to monitor its progress. Manual inspection is done regularly as well. Currently the parameters are hardcoded on lines 26, 27, 30, 44, 65, and 113.| Andrea Nesdoly |
|waveHMM.py| HMM development: A custom subclass that inherts the hmmlearn.base.BaseHMM methods, developed to utilize custom emission probability density functions. An example on how to use the subclass is provided at the bottom of the script. The initial, transition, and emission probabilities were derived through statistical analysis. Continuous probability distribution functions were fit the SOG profiles for the wildlife-viewing and non-viewing states, and the optimal probability distribution functions were fitted by minimizing the negative log-likelihood.| Andrea Nesdoly |
