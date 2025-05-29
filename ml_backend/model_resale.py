import pandas as pd
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def load_data():
    data = pd.read_csv("cleaned_data.csv")
    return data

def prepare_features(data):
    features = [
        "price",
        "review_score",
        "freight_value"
    ]
    target = "price"  # We're predicting resale price (same as original price)

    X = data[features]
    y = data[target]
    return X, y

def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def train_xgboost_regressor(X_train, y_train):
    param_grid = {
        'n_estimators': [100, 300],
        'max_depth': [6, 8],
        'learning_rate': [0.05, 0.1],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    xgb = XGBRegressor(random_state=42)
    grid_search = GridSearchCV(xgb, param_grid, cv=KFold(n_splits=5), n_jobs=-1)  # Changed StratifiedKFold to KFold
    grid_search.fit(X_train, y_train)

    best_xgb = grid_search.best_estimator_
    return best_xgb

def main():
    data = load_data()
    X, y = prepare_features(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training Linear Regression model...")
    lr_model = train_linear_regression(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    lr_mae = mean_absolute_error(y_test, lr_preds)
    print(f"Linear Regression MAE: {lr_mae:.4f}")

    print("Training XGBoost model...")
    xgb_model = train_xgboost_regressor(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    xgb_mae = mean_absolute_error(y_test, xgb_preds)
    print(f"XGBoost MAE: {xgb_mae:.4f}")

    # Save the better model (choose based on MAE or manually)
    if xgb_mae < lr_mae:
        joblib.dump(xgb_model, "resale_model.pkl")
        print("XGBoost model saved as 'resale_model.pkl'")
    else:
        joblib.dump(lr_model, "resale_model.pkl")
        print("Linear Regression model saved as 'resale_model.pkl'")

if __name__ == "__main__":
    main()