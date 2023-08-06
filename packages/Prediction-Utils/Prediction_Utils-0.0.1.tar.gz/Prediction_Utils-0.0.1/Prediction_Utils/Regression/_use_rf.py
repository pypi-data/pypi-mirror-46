__auther__ = 'Xinyu Wang'

from sklearn.ensemble import RandomForestRegressor
import sklearn.model_selection.train_test_split

def run_rf(X,y,cv=5,random_state=0,return_format='np'):
    regr = RandomForestRegressor(max_depth=2, random_state=0,
                                 n_estimators=100)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

    regr.fit(X_train, y_train)
    RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2,
                          max_features='auto', max_leaf_nodes=None,
                          min_impurity_decrease=0.0, min_impurity_split=None,
                          min_samples_leaf=1, min_samples_split=2,
                          min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=None,
                          oob_score=False, random_state=0, verbose=0, warm_start=False)
    print_time(regr.feature_importances_)
    return
