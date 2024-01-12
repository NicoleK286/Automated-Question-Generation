from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
import tensorflow as tf

from sherlock import helpers
from sherlock.features.preprocessing import extract_features, convert_string_lists_to_lists, prepare_feature_extraction
from sherlock.deploy.train_sherlock import train_sherlock
from sherlock.deploy.predict_sherlock import predict_sherlock
import pandas as pd

# Load test data and labels
test_samples = pd.read_parquet('../data/data/raw/test_values.parquet')
test_labels = pd.read_parquet('../data/data/raw/test_labels.parquet')

# Check if 'category' column exists in test_labels, and rename it if necessary
if 'category' not in test_labels:
    test_labels = test_labels.rename(columns={'type': 'category'})

# Encode labels using LabelEncoder
le = LabelEncoder()
y_test = le.fit_transform(test_labels['category'])

# Load Sherlock-ready test data
sher_ready = pd.read_csv("/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/test.csv")

# Join the sher_ready and test_labels dataframes using a common column
merged_df = pd.merge(sher_ready, test_labels, left_index=True, right_index=True)

# Convert the joined dataframe to lists format
test_samples_df2, y_test = convert_string_lists_to_lists(merged_df, "values", "category")
X_test2 = extract_features(test_samples_df2)

# Convert boolean columns to integer
for i in range(0, 1588):
    if X_test2.iloc[:, i].dtype == bool:
        X_test2.iloc[:, i] = X_test2.iloc[:, i].astype(int)

# Predict labels using Sherlock model
predicted_labels2 = predict_sherlock(X_test2, nn_id='sherlock')
sher_pred = predicted_labels2.tolist()

# Match predicted labels with row index from test.csv and print the output
sher_messages = []
for label in sher_pred:
    index = merged_df.index[merged_df['category'] == label][0]
    message = f"Meta category {label} is associated with row index {index}"
    sher_messages.append(message)
merged_df_columns = merged_df.columns
print(merged_df_columns)
sher2 = "\n".join(sher_messages)

# Convert category column to desired data type
test_labels['category'] = test_labels['category'].astype('int')

print(sher2)

# Print predicted labels
print(sher_pred)
