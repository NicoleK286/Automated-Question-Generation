import pandas as pd

def convert(x):
    x = x.transpose()
    li = x.values.tolist()
    import pandas as pd
    new = pd.DataFrame(columns=['values'])

    for i in range(0, len(li)):
        # Filter out null values before adding to the new DataFrame
        non_null_values = [value for value in li[i] if not pd.isna(value)]
        new.loc[len(new.index)] = [non_null_values]

    new.to_csv("test.csv")

    
    
    
