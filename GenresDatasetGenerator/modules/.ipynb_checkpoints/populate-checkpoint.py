import pandas as pd
from modules.create_sample import create_sample

def populate(data, r):
    
    columns = data.columns

    df = pd.DataFrame(columns=columns)

    i = 0
    for i in range(r):
        sample = create_sample(data)
        df = pd.concat([df, sample], ignore_index=True)
        i = i + 1


    populated_df = pd.concat([data, df])
    
    return populated_df