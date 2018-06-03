# Face-Entropy
This project has been created as a Final project for my B.A. in CS. The project attempts to find the actual security of state-of-the-art facial recognition technologies, and attempts to prove that they are vulnerable to complex brute-force attacks.


## Background

When dealing with biometric databases, the first question that needs to be asked is representation. We
chose the Dlib vector representation, which is an 128D vector that represents features of a certain face.


Two faces are considered similar if the euclidian distance between them is below a certain threshhold.
First of all, we plotted distances between faces of the same subject, to distances between facce of
different subjects:




As can be seen here, the ideal threshhold to minimize false-positives and true negatives lies around the 0.4
line. Note that this observation is dependant on the faces we tested against, Dlib recommends using a 0.6 distance.





## Running the csv file


```bash
workon facecourse-py3
python3 create_csv.py
deactivate
```
