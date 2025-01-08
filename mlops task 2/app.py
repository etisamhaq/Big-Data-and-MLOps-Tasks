import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def load_and_prepare_data(filename):

    df = pd.read_csv(filename, skiprows=[0])
    
    df = df.drop(['Sr#.', 'Roll No.', 'Name'], axis=1, errors='ignore')
    df = df.drop(['Sr. No.', 'Roll Number', 'Name'], axis=1, errors='ignore')
    
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(unnamed_cols, axis=1, errors='ignore')
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def predict_scores(train_df, test_df, start_activity=5):
    results = []
    
    feature_columns = train_df.columns[:-1]
    target_column = train_df.columns[-1]
    
    train_df = train_df.dropna(subset=[target_column])
    test_df = test_df.dropna(subset=[target_column])
    
    for i in range(start_activity, len(feature_columns) + 1):

        selected_features = feature_columns[:i]
        
        X_train = train_df[selected_features].fillna(0)  
        y_train = train_df[target_column]
        
        X_test = test_df[selected_features].fillna(0)  
        y_test = test_df[target_column]
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            'activities_used': i,
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2': r2
        })
    
    return pd.DataFrame(results)

ict_train = load_and_prepare_data('ICT Morning.csv')
cc_train = load_and_prepare_data('CC Morning.csv')

ict_test = load_and_prepare_data('ICT Afternoon.csv')
cc_test = load_and_prepare_data('CC Afternoon.csv')

ict_results = predict_scores(ict_train, ict_test)
cc_results = predict_scores(cc_train, cc_test)

print("ICT Course Predictions:")
print(ict_results)
print("\nCC Course Predictions:")
print(cc_results)