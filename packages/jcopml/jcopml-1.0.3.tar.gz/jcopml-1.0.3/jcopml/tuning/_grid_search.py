import numpy as np


class GridSearchParams:
    def __init__(self):
        self.rf_params = {
            "rf__n_estimators": [100, 150, 200],
            "rf__max_depth": [20, 50, 80],
            "rf__max_features": [0.3, 0.6, 0.8],
            "rf__min_samples_leaf": [1, 5, 10]
        }

        self.knn_params = {
            "knn__n_neighbors": np.arange(1, 31, 2),
            "knn__weights": ['uniform', 'distance'],
            "knn__p": [1, 1.5, 2]
        }

        self.svm_params = {
            "svm__gamma": np.logspace(-3, 3, 7),
            "svm__C": np.logspace(-3, 3, 7)
        }

        self.svm_imbalance_params = {
            "svm__gamma": np.logspace(-3, 3, 7),
            "svm__C": np.logspace(-3, 3, 7),
            "svm__class_weight": [{0: x, 1: 1-x} for x in [0.01, 0.3, 0.7, 0.99]]
        }

        self.xgb_params = {
            "xgb__max_depth": [3, 6, 10],
            "xgb__colsample_bytree": [0.4, 0.6, 0.8],
            "xgb__n_estimators": [100, 150, 200],
            "xgb__subsample": [0.4, 0.6, 0.8],
            "xgb__gamma": [1, 5, 10],
            "xgb__learning_rate": [0.01, 0.1, 1],
            "xgb__reg_alpha": [0.01, 0.1, 10],
            "xgb__reg_lambda": [0.01, 0.1, 10]
        }

        self.linreg_params = {
            "linreg__fit_intercept": [True, False]
        }

        self.enet_params = {
            "enet__fit_intercept": [True, False],
            "enet__alpha": np.logspace(-3, 2, 6),
            "enet__l1_ratio": [0, 0.25, 0.5, 0.75, 1]
        }

        self.logreg_params = {
            "logreg__fit_intercept": [True, False],
            "logreg__C": np.logspace(-3, 3, 7)
        }

        self.logreg_imbalance_params = {
            "logreg__fit_intercept": [True, False],
            "logreg__C": np.logspace(-3, 3, 7),
            "logreg__class_weight": [{0: x, 1: 1-x} for x in [0.01, 0.3, 0.7, 0.99]]
        }

        poly_params = {
            "poly__degree": [1, 2, 3],
            "poly__interaction_only": [True, False]
        }

        prep_poly_params = {
            "prep__numeric__poly__degree": [1, 2, 3],
            "prep__numeric__poly__interaction_only": [True, False]
        }

        self.rf_poly_params = {**poly_params, **self.rf_params}

        self.knn_poly_params = {**poly_params, **self.knn_params}

        self.svm_poly_params = {**poly_params, **self.svm_params}

        self.svm_imbalance_poly_params = {**poly_params, **self.svm_imbalance_params}

        self.xgb_poly_params = {**poly_params, **self.xgb_params}

        self.linreg_poly_params = {**poly_params, **self.linreg_params}

        self.enet_poly_params = {**poly_params, **self.enet_params}

        self.logreg_poly_params = {**poly_params, **self.logreg_params}

        self.logreg_imbalance_poly_params = {**poly_params, **self.logreg_imbalance_params}

        self.rf_prep_poly_params = {**prep_poly_params, **self.rf_params}

        self.knn_prep_poly_params = {**prep_poly_params, **self.knn_params}

        self.svm_prep_poly_params = {**prep_poly_params, **self.svm_params}

        self.svm_prep_imbalance_poly_params = {**prep_poly_params, **self.svm_imbalance_params}

        self.xgb_prep_poly_params = {**prep_poly_params, **self.xgb_params}

        self.linreg_prep_poly_params = {**prep_poly_params, **self.linreg_params}

        self.enet_prep_poly_params = {**prep_poly_params, **self.enet_params}

        self.logreg_prep_imbalance_poly_params = {**prep_poly_params, **self.logreg_imbalance_params}


grid_search_params = GridSearchParams()
