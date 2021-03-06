"""
    This file contains classification utilities to decide the current
    acition according to history.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import csv
import numpy as np
from sklearn import svm, preprocessing
import libpyAI as ai

def get_readings():
    """ Returns the  main  sensor readings """
    cl_enemy = ai.closestShipId()
    data = {}
    data["X"] = ai.selfX()
    data["Y"] = ai.selfY()
    data["VelX"] = ai.selfVelX()
    data["VelY"] = ai.selfVelY()
    data["RadarX"] = ai.selfRadarX()
    data["RadarY"] = ai.selfRadarY()
    data["Orientation"] = ai.selfHeadingDeg()
    data["ClosestRadarX"] = ai.closestRadarX()
    data["ClosestRadarY"] = ai.closestRadarY()
    data["ClosestItemX"] = ai.closestItemX()
    data["ClosestItemY"] = ai.closestItemY()
    data["EnemySpeed"] = ai.enemySpeedId(cl_enemy)
    data["EnemyX"] = ai.screenEnemyXId(cl_enemy)
    data["EnemyY"] = ai.screenEnemyYId(cl_enemy)
    data["EnemyHeading"] = ai.enemyHeadingDegId(cl_enemy)
    data["EnemyShield"] = ai.enemyShieldId(cl_enemy)
    data["EnemyDistance"] = ai.enemyDistanceId(cl_enemy)
    data["ShotAlert"] = ai.shotAlert(0)
    data["ShotDist"] = ai.shotDist(0)
    data["ShotVel"] = ai.shotVel(0)
    data["ShotVelDir"] = ai.shotVelDir(0)
    return data

def readData(f_name):
    """ Read history data from a csv file """
    data = []
    with open(f_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        first = True
        for row in reader:
            if first:
                header = row
                first = False
            else:
                data.append(row)
    return header, (data)


class classifier(object):
    """ Class used for classification of the current state """
    def __init__(self):
        self.scaler = preprocessing.StandardScaler()
        self.trained = False
        self.clf = svm.SVC(probability=True)
        self.headers = None

    def process(self, data):
        """ Extract labeled features from a matrix """
        idx_y = self.headers.index('Action')
        idx_shield = self.headers.index('EnemyShield')
        y = []
        X = []
        for row in data:
            line = []
            for value, i in zip(row, range(len(row))):
                if i == idx_y:
                    # Action column
                    y.append(value)
                elif i == idx_shield:
                    # Categorical variable
                    line.append(1.0 if value == 1 else 0.0)
                else:
                    line.append(value)
            X.append(line)
        X2 = np.array(X, dtype=np.float)

        # Select maximums per row which are not 1
        mask = (X2 == X2.max(axis=0)) & (X2 != 1.)

        # Convert all maximums and -1 (flag) values to the second maximum
        # We need it to properly represent our readings in a linear way
        # It happens that some maximums are just out of the scale of the rest of values
        X2[mask] = -1
        self.maxs = X2.max(axis=0)
        for i, max_el in zip(range(len(self.maxs)), self.maxs):
            X2[X2[:, i] == -1] = max_el

        if not self.trained:
            self.scaler.fit(X2)
        return self.scaler.transform(X2), y


    def extract_features(self, readings):
        """ Feature extraction of a given ship state """
        if not self.trained:
            raise NameError("""Attempt to extract features when classifier
                    is not trained""")

        features = []
        # Add features in the same order as in training
        for feature in self.headers:
            if feature == 'Action':
                continue
            elif feature == 'EnemyShield':
                features.append(1.0 if readings[feature] == 1 else 0)
            else:
                features.append(readings[feature])
        features = np.array(features)
        features = np.min((features, self.maxs), axis=0)
        return self.scaler.transform(features)


    def train(self, file_name='history.csv'):
        """ Train the classifier """
        fields, info = readData(file_name)
        self.headers = fields
        X, y = self.process(info)
        print("Fitting...")
        self.clf.fit(X,y)
        print("Fited!")
        self.trained = True


    def classify_state(self):
        """ Classifies the current ship state to give a proper action."""
        if not self.trained:
            return 'DoNothing', 1.0
        state = get_readings()
        X = self.extract_features(state)
        return str(self.clf.predict(X.reshape(1, -1))[0]), np.max(self.clf.predict_proba(X.reshape(1, -1)))

