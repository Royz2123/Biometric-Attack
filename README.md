# Face-Entropy

This project has been created as a Final Project for my B.A. in CS. The project attempts to find the enthropy of face feature spaces, and attempts to prove that they are vulnerable to brute-force attacks.


## Background

When dealing with biometric databases, the first question that needs to be asked is representation. We
chose the Dlib vector representation, which is an 128D vector that represents features of a certain face.


Two faces are considered similar if the euclidian distance between their representation is below a certain threshhold.
First of all, we plotted distances between faces of the same subject, to distances between facce of
different subjects:

![input image](https://github.com/Royz2123/Biometric-Attack/blob/master/figures/threshhold500.png)


As can be seen here, the ideal threshhold to minimize false-positives and true negatives lies around the 0.4
line. Note that this observation is dependant on the faces we tested against, Dlib recommends using a 0.6 distance.


After that, we were able to synthesize feature vectors of faces, and check them against a different database. We found that for around 1 million synthesized faces, we has around 80 hits (Around 0.001% hit ratio for 0.4 threshhold):

![input image](https://github.com/Royz2123/Biometric-Attack/blob/master/figures/diff_bases_10_mil.png)

Another interesting phenomenon is the rise in hits as a factor of the threshhold. Turns out that if we increase the threshhold by just a little we suddenly reach many more hits:

![input image](https://github.com/Royz2123/Biometric-Attack/blob/master/figures/thresh_test4.png)





## Setup

### Prerequisites

You will need to download the DLib library. We chose to install Dlib using a virtual enviroment, fro reference https://www.learnopencv.com/install-dlib-on-ubuntu/. Our code has been fitted to work on a virtualenv, on Ubuntu 16.04.


### Running examples

Note: All examples assume that the setup has been set with a virtual enviroment as described in "prerequsites". If you have obtained Dlib in some other way, or perhaps are just running from the default csv files provided, remove the "workon" and "deactivate" lines from the bash examples.

#### Example 1 - default run

Running the code with all the default parameters is done in the following way:

```bash
workon facecourse-py3
python3 attack_database.py
deactivate
```

Note that this examples has been provided as a bash file (run.sh):


#### Example 2 - specifying an attack size

```bash
workon facecourse-py3
python3 attack_database.py --attack-size 1000000
deactivate
```


#### Example 3 - specifying a new threshhold

For testing purposes, playing around with the threshhold can be done as follows:

```bash
workon facecourse-py3
python3 attack_database.py --threshhold 0.6
deactivate
```


#### Example 4 - using an existing seed, from a previous run

We make recovering a previous run super simple. Find the run that you wish to obtain it's random seed, and copy its recovery time (Either copy from filename or take first field of log file)


For Example, for the timestamp "05:06:2018_17:12:09", the code can be run as such:

```bash
workon facecourse-py3
python3 attack_database.py --recover-time 05:06:2018_17:12:09
deactivate
```
