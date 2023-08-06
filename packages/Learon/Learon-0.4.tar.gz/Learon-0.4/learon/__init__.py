from sklearn import tree as tr


class Classifier:
    def __init__(self):

        self.tree = None
        self.features = {"other": 0}
        self.labels = {}

    def train(self, dataset):
        sample = [
            [
                ["yellow", 140, "smooth"],
                "apple"
            ],
            [
                ["orange", 150, "bumpy"],
                "orange"
            ],
            [
                ["green", 140, 'smooth'],
                "apple"
            ]
        ]

        examples_features = []
        examples_labels = []

        for exemple in dataset:
            features_in_sample = []
            for feature in exemple[0]:
                try:
                    f = float(feature)
                except:
                    if feature in self.features.keys():
                        f = self.features[feature]
                    else:
                        self.features[feature] = len(self.features.keys())
                        f = self.features[feature]
                features_in_sample.append(f)
            examples_features.append(features_in_sample)
            label = exemple[1]
            try:
                f = float(label)
            except:
                if label in self.labels.keys():
                    f = self.labels[label]
                else:
                    self.labels[label] = len(self.labels.keys())
                    f = self.labels[label]
            examples_labels.append(f)

        print('Features : ')
        print(examples_features)
        print(self.features)
        print('Labels : ')
        print(examples_labels)
        print(self.labels)
        clf = tr.DecisionTreeClassifier()
        clf.fit(examples_features, examples_labels)
        self.tree = clf

    def predict(self, features):
        final_features = list()
        for feature in features:
            try:
                f = float(feature)
            except:
                if feature in self.features:
                    f = self.features[feature]
                else:
                    f = self.features["other"]
            final_features.append(f)
        prediction = self.tree.predict([final_features])
        return list(self.labels.keys())[int(prediction)]


def GenDatasetFromFile(path):
    import os
    dataset = []
    if os.path.isfile(path):
        file = open(path, 'r')
        f_content = file.read().split("=")[1]

        file.close()
        print("=====")
        features_l = []
        labels = []
        number = 0
        for line in f_content.split('\n'):
            if len(line) > 2:
                if int(number / 2) == float(number / 2):
                    features_l.append(line)
                else:
                    labels.append(line)
                number += 1

        print(features_l)
        print(labels)
        print("=====")

        for features, label in zip(features_l, labels):
            features = (features.split(' '))
            print(features)
            print(label)
            dataset.append([features, label])
        return dataset



