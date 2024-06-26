
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
import tensorflow as tf

from sherlock import helpers
from sherlock.features.preprocessing import extract_features, convert_string_lists_to_lists, prepare_feature_extraction
from sherlock.deploy.train_sherlock import train_sherlock
from sherlock.deploy.predict_sherlock import predict_sherlock
import pandas as pd
test_samples = pd.read_parquet('../data/data/raw/test_values.parquet')
test_labels = pd.read_parquet('../data/data/raw/test_labels.parquet')
sher_ready = pd.read_csv("/N/u/nickoshy/Carbonate/Sherlock/sherlock-project-master/QGD/test.csv")
try:
    test_labels['category']
except KeyError:
    test_labels = test_labels.rename(columns={'type': 'category'})

test_samples_df2, y_test = convert_string_lists_to_lists(sher_ready, test_labels, "values", "category")
X_test2 = extract_features(test_samples_df2)
for i in range(0,1588):
    if( X_test2.iloc[:,i].dtype == bool):
        X_test2.iloc[:,i] = X_test2.iloc[:,i].astype(int)

predicted_labels2 = predict_sherlock(X_test2, nn_id='sherlock')
sher_pred = predicted_labels2.tolist()

sher_messages = []
for label in sher_pred:
    index = test_labels.index[test_labels['category'] == label][0]
    message = f"Meta category {label} is associated with row index {index}"
    sher_messages.append(message)
sher2 = "\n".join(sher_messages)
print(sher2)
    
print (sher_pred)





try:
    test_labels['category']
except KeyError:
    test_labels = test_labels.rename(columns={'type': 'category'})

# Join the sher_ready and test_labels dataframes using a common column
merged_df = pd.merge(sher_ready, test_labels, left_index=True, right_index=True)

# Convert the joined dataframe to lists format
test_samples_df2, y_test = convert_string_lists_to_lists(merged_df, "values", "category")
X_test2 = extract_features(test_samples_df2)

for i in range(0,1588):
    if( X_test2.iloc[:,i].dtype == bool):
        X_test2.iloc[:,i] = X_test2.iloc[:,i].astype(int)

predicted_labels2 = predict_sherlock(X_test2, nn_id='sherlock')
sher_pred = predicted_labels2.tolist()

sher_messages = []
for label in sher_pred:
    index = merged_df.index[merged_df['category'] == label][0]
    message = f"Meta category {label} is associated with row index {index}"
    sher_messages.append(message)
sher2 = "\n".join(sher_messages)
print(sher2)

print(sher_pred)

