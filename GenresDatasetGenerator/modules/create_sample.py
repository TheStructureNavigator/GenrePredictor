import pandas as pd
import random as rnd

def create_sample(data):
    
    data_df = data[data.columns]
    features = data_df.columns
    
    random_features = []
    for feature in features:
        p25 = data_df[feature].describe()[4]
        p75 = data_df[feature].describe()[6]
        random_value = rnd.uniform(p25, p75)
        random_features.append(random_value)
   
    sample = pd.DataFrame(data=[random_features], columns=features)
    sample[['key', 'mode', 'time_signature']] = sample[['key', 'mode', 'time_signature']].astype(int)
    
    return sample
