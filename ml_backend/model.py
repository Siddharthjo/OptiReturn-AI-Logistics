import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import joblib

# Load the cleaned data
data = pd.read_csv("cleaned_data.csv")
data = data.head(3000)

# Encode categorical columns
data_encoded = pd.get_dummies(data, columns=["customer_city", "customer_state"])

# Features and target
X = data_encoded.drop(columns=["order_id", "product_id", "return_flag"])
y = data_encoded["return_flag"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Random Forest Grid Search
rf_grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid={
        'n_estimators': [100, 200],
        'max_features': ['sqrt', 'log2'],
        'max_samples': [0.8, 1.0]
    },
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='roc_auc',
    n_jobs=-1
)
rf_grid.fit(X_train, y_train)
rf_best = rf_grid.best_estimator_
joblib.dump(rf_best, "rf_model.pkl")

# XGBoost Grid Search
xgb_grid = GridSearchCV(
    XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
    param_grid={
        'n_estimators': [100, 200],
        'max_depth': [4, 6],
        'learning_rate': [0.05, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    },
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='roc_auc',
    n_jobs=-1
)
xgb_grid.fit(X_train, y_train)
xgb_best = xgb_grid.best_estimator_
joblib.dump(xgb_best, "xgb_model.pkl")

# Evaluate performance
rf_auc = roc_auc_score(y_test, rf_best.predict_proba(X_test)[:, 1])
xgb_auc = roc_auc_score(y_test, xgb_best.predict_proba(X_test)[:, 1])
print(f"Random Forest AUC: {rf_auc:.4f}")
print(f"XGBoost AUC: {xgb_auc:.4f}")

print("✅ Models saved: rf_model.pkl and xgb_model.pkl")