def convert(x):
    x = x.transpose()
    li = x.values.tolist()
    import pandas as pd
    new = pd.DataFrame(columns = ['values'])
    for i in range(0,len(li)):
        new.loc[len(new.index)] = [li[i]]
    new.to_csv("test.csv")


    
    
    
