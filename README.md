# Whale-watchin AIS Vessel movement Evaluation Project Public Repository
By: Andrea Nesdoly (nesdolya@uvic.ca)
SURREAL & CORAL Groups, University of Victoria, Department of Geography

## WAVE Project
The WAVE Project's goals are to understand whale-watching activities using Automatic Identification System (AIS), and to determine the feasibility of utilizing AIS data as a tool for informing whale-watching operations, vessel traffic management, conservation, and policy.

Please visit the WAVE Project website to learn more: https://waveproject.ca/

## Modelling marine vessels engaged in wildlife-viewing behaviour using Automatic Identification Systems (AIS)
Andrea Nesdoly Master of Science Thesis work

The WAVE Project has afforded an opporuntity to model whale-watching vessel behavior with AIS and classify this behaviour. The MSc student (Andrea Nesdoly/myself) has tested three established classification models to find when the vessels are observing wildlife and when they are not. One of these successful models was then deployed to determine if behavior classification utlizing machine learning is feasible when scaled up to the whole whale-watching vessel fleet surrounding Vancouver Island, Coastal British Columbia.

### Scripts and Notebooks
The scripts used in this research were developed using Anaconda and Python 3.8 and 3.9. Established Python libraries were utilized such as:
- [scikit-learn](https://scikit-learn.org/stable/)
- [scipy](https://scipy.org/)

## Table of Scripts and Notebooks
|Name|Description|Collaborators|
|----|-----------|-------------|
|listen_aishub.py| A script developed to listen to the incoming stream of AIS data from AISHub, a crowdsourced data streaming platform. This basic script runs indefinately, storing each days AIS NMEA format data as a text file. Each month is then archived in a .zip folder. This program is currently running on a cloud server using supervisord to monitor its progress. Manual inspection is done regularly as well. Currently the parameters are hardcoded on lines 26, 27, 30, 44, 65, and 113.| Andrea Nesdoly |
|----|-----------|-------------|
