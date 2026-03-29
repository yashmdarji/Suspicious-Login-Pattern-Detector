import joblib
import pandas as pd

def run_detector():
    model = joblib.load('models/account_takeover_detector.joblib')
    required_features = joblib.load('models/model_features.joblib')

    sample_login_data = [[1,1,1,1,1,0]]
    input_df = pd.DataFrame(sample_login_data, columns=required_features)
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]

    if prediction[0] == 1:
        print(f"\n[ALERT] High Risk! Takeover Probability: {probability*100:.2f}%")
        print("Action: Block login and trigger OTP verification.")
    else:
        print(f"\n[INFO] Login Safe. Confidence: {(1-probability)*100:.2f}%")

if __name__ == "__main__":
    run_detector()