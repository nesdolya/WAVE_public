# WAVE Public
## Public scripts and results for the WAVE Project
Scripts and results that can be made available will be posted here by the end of 2021.

The WAVE Project's goals are to understand whale-watching activities using Automatic Identification System (AIS), and to determine the feasibility of utilizing AIS data as a tool for informing whale-watching operations, vessel traffic management, conservation, and policy.

The high level results of the terrestrial and satellite AIS case study can be found here: https://waveproject.ca/2020/06/24/automatic-identification-system-ais-receiver-comparison/

Please visit the WAVE Project website to learn more:https://waveproject.ca/

The WAVE Project has afforded an opporuntity to model whale-watching vessel behavior with AIS and classify this behaviour. The MSc student (Andrea Nesdoly/myself) has tested three established classification models to find when the vessels are observing wildlife and when they are not. One of these successful models will be deployed in a machine learning capacity to determine if behavior classification is feasible when scaled up and/or in real-time.

When this research reached publication the model code will be shared here for other researchers to use.


## Scripts
|Name|Description|Collaborators|
|----|-----------|-------------|
|listen_aishub.py| A script developed to listen to the incoming stream of AIS data from AISHub, a crowdsourced data streaming platform. This basic script runs indefinately, storing each days AIS NMEA format data as a text file. Each month is then archived in a .zip folder. This program is currently running on a cloud server using supervisord to monitor its progress. Manual inspection is done regularly as well. Currently the parameters are hardcoded on lines 26, 27, 30, 44, 65, and 113.| - |
