from modules.authenticator import authenticator
from modules.get_info import get_info
from modules.extract_data import extract_data
import os

def extractor(sp, urls, save=False, df_name="track_data"):

    #Initialize Spotify user credentials
    sp = authenticator()

    print('#---Extracting data---#')
    info_dict, url_types = get_info(sp, urls)
    df = extract_data(sp, info_dict, url_types)
    print('|-------Finished------|')
    print('#---------------------#')

    #Check for duplicates and remove them
    print('#Checking for duplicates#')
    #Convert rows to tuples beacuse lists are not hashable
    df_tuple = df.apply(tuple, axis=1) 
    duplicates = df_tuple.duplicated()
    if duplicates.any():

        print("Removing duplicates from the DataFrame.")
        df = df[~duplicates]
        print('|-------Finished------|')
        print('#---------------------#')
    if save:
        
        print('#Saving file#')
        folder_name = "dataframes"
        os.makedirs(folder_name, exist_ok=True)
        file_path = os.path.join(folder_name, f"{df_name}.csv")
        df.to_csv(file_path, index=False)
        print(f"DataFrame saved to {file_path}.")

    return df