# Face-Entropy
This project has been created as a Final project for my B.A. in CS. The project attempts to find the actual security of state-of-the-art facial recognition technologies, and attempts to prove that they are vulnerable to complex brute-force attacks.


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





## Running the attack


```bash
workon facecourse-py3
python3 attack_database.py
deactivate
```
