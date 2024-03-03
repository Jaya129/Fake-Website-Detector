import numpy as np
import pandas as pd
import pickle
import time

from random_forest import RandomForest

Dataset = "dataset_full_copy.csv"

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return round(accuracy, 4)

# 3) load with np.genfromtxt()
data = np.genfromtxt(Dataset, delimiter=",", dtype=np.int32)
# print(data.shape)

# split into X and y
n_samples, n_features = data.shape
n_features -= 1
X = data[:, 0:n_features]
y = data[:, n_features]
# print(X.shape, y.shape)
# print(X[0, 0:5])

# Timer start
start_time = time.time()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)

classifier = RandomForest(n_trees=21, max_depth=6)
# classifier = RandomForest(n_trees=12, max_depth=6)

classifier.train(X_train, y_train)
y_pred = classifier.prediction(X_test)
acc = accuracy(y_test, y_pred) * 100
print (f"Random Forest Accuracy: {acc}")

from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
cm = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix : \n {cm}")
f1 = f1_score(y_test, y_pred) * 100
# print(f"f1 score : {f1}")

# Display render time
elapsed_time = time.time() - start_time
print(time.strftime("Render Time : %H:%M:%S", time.gmtime(elapsed_time)))

# pickle
# pickle.dump(classifier, open('model_RF.pkl','wb'))