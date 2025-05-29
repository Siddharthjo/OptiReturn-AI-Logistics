import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
import joblib

def load_data():
    data = pd.read_csv("cleaned_data.csv")
    return data

def prepare_features(data):
    features = [
        "price",
        "delivery_time",
        "low_price",
        "high_density_city",
        "review_score",
        "freight_value"
    ]
    target = "return_flag"

    X = data[features]
    y = data[target]
    return X, y

def train_random_forest(X_train, y_train):
    param_grid = {
        'n_estimators': [100, 300],
        'max_depth': [6, 8],
        'max_features': [3, 5]
    }

    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf, param_grid, cv=StratifiedKFold(5), scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_rf = grid_search.best_estimator_
    return best_rf

def train_xgboost(X_train, y_train):
    param_grid = {
        'n_estimators': [100, 300],
        'max_depth': [6, 8],
        'learning_rate': [0.05, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    grid_search = GridSearchCV(xgb, param_grid, cv=StratifiedKFold(5), scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_xgb = grid_search.best_estimator_
    return best_xgb

def main():
    data = load_data()
    X, y = prepare_features(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("Training Random Forest...")
    rf_model = train_random_forest(X_train, y_train)
    rf_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test)[:, 1])
    print(f"Random Forest AUC: {rf_auc:.4f}")

    print("Training XGBoost...")
    xgb_model = train_xgboost(X_train, y_train)
    xgb_auc = roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1])
    print(f"XGBoost AUC: {xgb_auc:.4f}")

    # Save the better model (choose manually or use higher AUC)
    if xgb_auc > rf_auc:
        joblib.dump(xgb_model, "rf_return_model.pkl")
        print("XGBoost model saved as 'rf_return_model.pkl'")
    else:
        joblib.dump(rf_model, "rf_return_model.pkl")
        print("Random Forest model saved as 'rf_return_model.pkl'")

if __name__ == "__main__":
    main()