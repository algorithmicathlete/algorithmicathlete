import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, \
    classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


def split_data(test_size):
    df = pd.read_csv("play_data.csv")
    X = df.drop(columns=['target', 'defteam', 'posteam'])
    y = df['target']

    X = X.dropna()
    y = y.loc[X.index]

    return train_test_split(
        X, y, test_size=test_size, stratify=y
    )

features = [
    'down', 'ydstogo', 'yardline_100', 'score_differential', 'half_seconds_remaining', 'shotgun'
]

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = split_data(test_size=0.2)
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=200, class_weight="balanced"))
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall   :", recall_score(y_test, y_pred))
    print("F1 Score :", f1_score(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    coefs = clf.named_steps['logisticregression'].coef_[0]
    importance = sorted(zip(features, coefs), key=lambda x: abs(x[1]), reverse=True)

    print("\nFeature Importance:")
    for f, c in importance:
        print(f, c)