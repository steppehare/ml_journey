# Наступний — Крок 3: train.py. По roadmap треба:

# Взяти df з engineering() і розділити на features X і target y
# train_test_split з shuffle=False (важливо для timeseries)
# Натренувати RandomForestClassifier
# Вивести в консоль: accuracy, F1, ROC-AUC
# Зберегти модель: joblib.dump(model, "models/rf_v1.joblib")