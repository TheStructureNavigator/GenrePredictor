#Common Dependencies
import pandas as pd
import random as rnd
import seaborn as sns
import matplotlib.pyplot as plt
#Raw Data Extractor
from modules.authenticator import authenticator
from modules.get_info import get_info
from modules.extract_features import extract_features
#Data Editor
from modules.create_sample import create_sample
from modules.populate import populate

import streamlit as st

#Spotify User Credentials
sp = authenticator()

pd.set_option('display.max_rows', 10)
plt.style.use('seaborn-v0_8')

#Functions
#Function to load CSV file and return dataframe
def load_data(file):
    df = pd.read_csv(file)
    return df

#Function to save dataframe to CSV file
def save_data(dataframe, path):
    dataframe.to_csv(path)

# Streamlit app
def main():
    ################################################################
    #Raw Data Extractor
    #################################################################

    #Description
    st.header('Raw Data Extractor')
    st.markdown(
        """
        __Extract audio features in raw format as an 
        input to an neural network__
        """)
    #-------------------------------------------------------------

    #Checkbox to hide/unhide the "Data Extractor" section
    show_data_extractor = st.expander("__Provide URLs and extract data__")
    #-------------------------------------------------------------

    with show_data_extractor:
        # Set title and description
        st.markdown("Provide Spotify URLs and extract")

        # User input
        url_input = st.text_input("Enter Spotify URLs (separated by commas)")
        urls = url_input.split(",")

        # Extract data on button click
        if st.button("Extract Data"):
            # Validate input
            if len(urls) == 0 or all(url.strip() == "" for url in urls):
                st.warning("Please enter at least one URL.")
            else:
                #Extract URI from links
                print('Extracting URIs from links...')
                info_dict, url_types = get_info(sp, urls)
                print('............................')
                print('URIs have been extracted\n')

                #Extract data from URIs
                print('Extracting data...')
                dataframe = extract_features(sp, info_dict, url_types)
                print('............................')
                print('Data has been extracted\n')

                #Remove duplicates
                print('Number of duplicates:', dataframe.duplicated().sum())
                if dataframe.duplicated().sum() > 0:
                    print('Removing duplicates...')
                    dataframe = dataframe.drop_duplicates()
                    print('Duplicates have been removed')
                    print('Number of duplicates:', dataframe.duplicated().sum())

            if 'extracted_data' not in st.session_state:
                st.session_state['extracted_data'] = pd.DataFrame()

            st.session_state['extracted_data'] = dataframe

        if 'extracted_data' in st.session_state:

            if st.checkbox('Show extracted data'):

                st.dataframe(st.session_state['extracted_data'])

                save_extracted_dataframe = st.button('Save Extracted Dataframe')

                if save_extracted_dataframe:
                    save_data(
                        st.session_state['extracted_data'], 'Albums/test.csv')
                    st.write("Extracted Data has been saved.")
                    st.write("File saved in Albums/test.csv'.")
    
    st.divider()

    ################################################################
    #Loader
    #################################################################
    st.header('Data Loader')
    st.markdown(
        """
        __Load data to edit__
        """)

    # Checkbox to hide/unhide the "Data loader" section
    show_data_loader = st.expander("__Load Data__")

    with show_data_loader:

        # File upload
        uploaded_file = st.file_uploader(
            "Upload a CSV file that contains a prepared dataframe:", type=["csv"])

        if uploaded_file is not None:
            # Load DataFrame from uploaded file
            loaded_df = load_data(uploaded_file)
            if 'Unnamed: 0' in loaded_df.columns:
                loaded_df = loaded_df.drop(columns='Unnamed: 0')

            # Initialize session state
            if 'loaded_data' not in st.session_state:
                st.session_state['loaded_data'] = pd.DataFrame()

            # Update session state
            st.session_state['loaded_data'] = loaded_df

            # Initialize session state
            if 'editable_data' not in st.session_state:
                st.session_state['editable_data'] = pd.DataFrame()

            # Update session state
            st.session_state['editable_data'] = loaded_df.copy()

            # Checkbox to toggle visibility of original DataFrame
            show_original = st.checkbox("Show Loaded Data")

            if show_original:

                # Create tabs for Original DataFrame and Additional Summary
                tab1, tab2 = st.tabs(["Loaded Data", "Additional Summary"])

                with tab1:
                    st.dataframe(st.session_state['loaded_data'])
                    st.divider()

                with tab2:
                    num_rows = len(st.session_state['loaded_data'])
                    st.write(f"Number of Rows: {num_rows}")
                    num_columns = len(
                        st.session_state['loaded_data'].columns)
                    st.write(f"Number of Columns: {num_columns}")
                    st.write(st.session_state['loaded_data'].describe())
    st.divider()

    ################################################################
    #Data Editor
    #################################################################
    st.header('Data Editor')
    st.markdown(
        """
        __Choose from available methods and modify data__

        - Features Extracting - Calculate additional features
        - Populating Median Neighbourhood - Populate with additional samples
        - Kernel Density Estimation Trimming - Remove outliers by feature

        __To modify method parameters, look into code__
        """)

    if 'loaded_data' in st.session_state:
        
        #Session state variable
        dataframe = st.session_state['editable_data']

        # Checkbox to hide/unhide the "method" section
        show_features = st.expander("__Features Extracting__")

        with show_features:
            
            st.write('To add or modify calculated features, look into code')
            
            if st.button('Add new features'):

                #Calculate and add additional features columns
                dataframe['danceability_energy_ratio'] = dataframe['danceability'] * dataframe['energy']
                dataframe['danceability_valence_ratio'] = dataframe['danceability'] * dataframe['valence']

                st.write('New features has been added')
                
                # Update session state
                st.session_state['editable_data'] = dataframe

        # Checkbox to hide/unhide the "method" section
        show_populating = st.expander("__Populating Median Neighbourhood__")

        with show_populating:

            st.write('To change number of new samples to populate, look into code')
            
            #Number of samples
            n = 1000

            if st.button('Populate with additional data'):
                
                st.write('Actual shape:', dataframe.shape)
                st.write('............................')
                st.write('Populating...')

                dataframe = populate(dataframe.select_dtypes(include='number'), n)
                st.write('Populating has been done')
                st.write('............................')

                # Update session state
                st.session_state['editable_data'] = dataframe
                st.write('Shape after populating:', st.session_state['editable_data'].shape)

        # Checkbox to hide/unhide the "method" section
        show_kde_trim = st.expander("__Kernel Density Estimation Trimming__")

        with show_kde_trim:

            st.write('To change trim range, look into code')

            if st.button('Trim outliers'):
                # Create a figure for the plots
                fig, axes = plt.subplots(1, 2, figsize=(12, 6))

                # KDE plot for feature before trimming
                sns.kdeplot(data=dataframe, x='danceability', bw_adjust=0.5, ax=axes[0])
                axes[0].set_xlabel('Danceability')
                axes[0].set_ylabel('Density')
                axes[0].set_title('KDE Plot Before Trimming')

                # Trim features
                dataframe = dataframe[(dataframe['danceability'] > 0.5) & (dataframe['danceability'] < 0.7)]

                st.write('Data has been trimmed')

                # Update session state
                st.session_state['editable_data'] = dataframe

                # KDE plot for feature after trimming
                sns.kdeplot(data=dataframe, x='danceability', bw_adjust=0.5, ax=axes[1])
                axes[1].set_xlabel('Danceability')
                axes[1].set_ylabel('Density')
                axes[1].set_title('KDE Plot After Trimming')

                # Display the plots on Streamlit
                st.pyplot(fig)

        # Checkbox to hide/unhide the "method" section
        show_add_genre = st.expander("__Add Genre Column__")

        with show_add_genre:

            st.write('To change name of a genre, look into code')

            if st.button('Add Genre'):

                dataframe['genres'] = 'classical'

                # Update session state
                st.session_state['editable_data'] = dataframe

        #Show edited dataframe
        st.write('Edited Dataframe')
        st.dataframe(st.session_state['editable_data'])

        save_edited_dataframe = st.button('Save Edited Dataframe')
        
        if save_edited_dataframe:
            path = 'Genres/AlternativeGenre_pop.csv'
            save_data(dataframe, path)
            st.write("Extracted Data has been saved.")
            st.write(path)

    else:
        
        load_first = st.expander('LOAD DATA FIRST')
        
        with load_first:
            st.write('There is no data to edit')






# Run the app
if __name__ == "__main__":
    main()