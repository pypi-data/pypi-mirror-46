import pandas as pd


class ForecastFlow(object):
    def __init__(self, classificator, model_map):
        self.classificator = classificator
        self.model_map = model_map

    def predict(self, x):
        classified = self.classify(x.copy())

        frames = []
        for k, v in self.model_map:
            group = classified[classified["CLASSIFICATION"] == k]
            if not group.empty:
                predicted = v.predict(group)
                frames.append(predicted)

        concatenated = pd.concat(frames)
        concatenated = concatenated.sort_index(axis=0)

        return concatenated["PREDICTED"]

    def classify(self, x: pd.DataFrame):
        classification = self.classificator.classify(x)
        x["CLASSIFICATION"] = classification
        return x
