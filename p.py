
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv("credit_risk_dataset (1).csv")

# Missing values
df.fillna(df.median(numeric_only=True), inplace=True)
df.drop_duplicates(inplace=True)

# Outlier detection
cols = [
    "person_age",
    "person_income",
    "person_emp_length",
    "loan_amnt",
    "loan_int_rate",
    "loan_percent_income",
    "cb_person_cred_hist_length"
]

q1 = df[cols].quantile(0.25)
q3 = df[cols].quantile(0.75)

IQR = q3 - q1

lower = q1 - 1.5 * IQR
upper = q3 + 1.5 * IQR

count = ((df[cols] < lower) | (df[cols] > upper)).sum()

df = df[
    ((df[cols] >= lower) & (df[cols] <= upper)).all(axis=1)
]

# Separate categorical columns
text_cols = df.select_dtypes(include="object").columns

# OneHotEncoding
encoder = OneHotEncoder(handle_unknown="ignore")

encoder_data = encoder.fit_transform(df[text_cols])

encoded_df = pd.DataFrame(
    encoder_data.toarray(),
    columns=encoder.get_feature_names_out(text_cols),
    index=df.index
)

# Numerical columns
numeric_df = df.drop(columns=list(text_cols) + ["loan_status"])

# Combine numerical and encoded columns
features = pd.concat([numeric_df, encoded_df], axis=1)

target = df["loan_status"]

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.2,
    random_state=100,
    stratify=target
)

# Feature scaling
scaler = StandardScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

models={
    "Logistic Regression":LogisticRegression(
        max_iter=1000,
        C=1.0,
        class_weight="balanced"
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        random_state=100
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=100
    )
}

for name,model in models.items():
    model.fit(x_train, y_train)

    # Predictions
    y_pred = model.predict(x_test)

    # Model evaluation
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    version = "v1"
    filename = f"{name.replace(' ', '_').lower()}_{version}.pkl"
    joblib.dump(model, filename)
    print(f"{name} saved as {filename}")

joblib.dump(encoder, "encoder_v1.pkl")
joblib.dump(scaler, "scaler_v1.pkl")