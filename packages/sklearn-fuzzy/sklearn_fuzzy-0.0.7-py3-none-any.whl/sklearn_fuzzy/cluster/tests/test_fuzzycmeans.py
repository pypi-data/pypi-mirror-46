from sklearn_fuzzy.cluster import FuzzyCMeans

import numpy as np

X = np.array([[1, 2], [1, 4], [1, 0],
              [10, 2], [10, 4], [10, 0]])

fcm = FuzzyCMeans(n_clusters=2, m=2, seed=0).fit(X)
print(fcm.labels_)
print(fcm.predict(np.array([[0, 0], [12, 3]])))
print(fcm.cluster_centers_)
