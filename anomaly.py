from sklearn.ensemble import IsolationForest
import numpy as np

def check_anomaly(plate):

    data = np.array([
        [200,100,10],
        [250,120,12],
        [180,90,8],
        [220,110,10],
        [210,105,11]
    ])

    model = IsolationForest(contamination=0.2)
    model.fit(data)

    test = plate[["length","width","thickness"]].values

    pred = model.predict(test)

    if pred[0]==-1:
        return "Warning: unusual design"

    return "Design looks normal"