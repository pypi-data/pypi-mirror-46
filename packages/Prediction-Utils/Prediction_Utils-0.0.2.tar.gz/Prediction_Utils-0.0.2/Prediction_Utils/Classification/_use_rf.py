__auther__ = 'Xinyu Wang'

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

def run_CrossValidation(X,y,cv=5,random_state=0,max_depth=2,n_estimators=100):
    clf=RandomForestClassifier(n_estimators=100,max_depth=max_depth)
    scores = cross_val_score(clf, X, y, cv=5)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    clf.fit(X,y)
    return clf.feature_importances_
