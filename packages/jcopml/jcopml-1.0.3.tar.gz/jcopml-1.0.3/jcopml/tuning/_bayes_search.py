from skopt.space import Real, Integer, Categorical


class BayesSearchParams:
    def __init__(self):
        self.rf_params = {
            "rf__n_estimators": Integer(100, 200),
            "rf__max_depth": Integer(20, 80),
            "rf__max_features": Real(0.1, 1),
            "rf__min_samples_leaf": Integer(1, 20)
        }

        self.knn_params = {
            "knn__n_neighbors": Integer(1, 40),
            "knn__weights": Categorical(['uniform', 'distance']),
            "knn__p": Real(1, 2)
        }

        self.svm_params = {
            "svm__gamma": Real(0.001, 1000, prior='log-uniform'),
            "svm__C": Real(0.001, 1000, prior='log-uniform')
        }

        self.xgb_params = {
            "xgb__max_depth": Integer(1, 10),
            "xgb__learning_rate": Real(0.01, 1, prior='log-uniform'),
            "xgb__n_estimators": Integer(100, 200),
            "xgb__subsample": Real(0.3, 0.8),
            "xgb__gamma": Integer(1, 10),
            "xgb__colsample_bytree": Real(0.1, 1),
            "xgb__reg_alpha": Real(0.001, 10, prior='log-uniform'),
            "xgb__reg_lambda": Real(0.001, 10, prior='log-uniform')
        }

        self.linreg_params = {
            "linreg__fit_intercept": Categorical([True, False])
        }

        self.enet_params = {
            "enet__fit_intercept": Categorical([True, False]),
            "enet__alpha": Real(0.0001, 100, prior='log-uniform'),
            "enet__l1_ratio": Real(0, 1)
        }

        self.logreg_params = {
            "logreg__fit_intercept": Categorical([True, False]),
            "logreg__C": Real(0.001, 1000, prior='log-uniform')
        }

        poly_params = {
            "poly__degree": Integer(1, 3),
            "poly__interaction_only": Categorical([True, False])
        }

        prep_poly_params = {
            "prep__numeric__poly__degree": Integer(1, 3),
            "prep__numeric__poly__interaction_only": Categorical([True, False])
        }

        self.rf_poly_params = {**poly_params, **self.rf_params}

        self.knn_poly_params = {**poly_params, **self.knn_params}

        self.svm_poly_params = {**poly_params, **self.svm_params}

        self.xgb_poly_params = {**poly_params, **self.xgb_params}

        self.linreg_poly_params = {**poly_params, **self.linreg_params}

        self.enet_poly_params = {**poly_params, **self.enet_params}

        self.logreg_poly_params = {**poly_params, **self.logreg_params}

        self.rf_prep_poly_params = {**prep_poly_params, **self.rf_params}

        self.knn_prep_poly_params = {**prep_poly_params, **self.knn_params}

        self.svm_prep_poly_params = {**prep_poly_params, **self.svm_params}

        self.xgb_prep_poly_params = {**prep_poly_params, **self.xgb_params}

        self.linreg_prep_poly_params = {**prep_poly_params, **self.linreg_params}

        self.enet_prep_poly_params = {**prep_poly_params, **self.enet_params}

        self.logreg_prep_poly_params = {**prep_poly_params, **self.logreg_params}


bayes_search_params = BayesSearchParams()
