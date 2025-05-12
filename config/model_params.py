from scipy.stats import randint, uniform

LIGHTGBM_PARAMS = {
    'n_estimators' : randint(100,500),
    'max_depth' : randint(5,50),
    'learning_rate' : uniform(1e-2, 2e-1),
    'boosting_type' : ['gbdt', 'dart', 'goss'],
}

RANDOM_SEARCH_PARAMS = {
    'n_iter' : 5,
    'cv' : 5,
    'n_jobs' : -1,
    'verbose' : 2,
    'random_state' : 11,
    'scoring' : 'accuracy'
}
