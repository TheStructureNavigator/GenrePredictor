import streamlit as st

# Streamlit app
def main():
    # Set title and description
    st.title("Spotify URL Data Extractor")
    st.markdown("Enter Spotify URLs to extract data.")

    # User input
    url_input = st.text_input("Enter Spotify URLs (separated by commas)")
    urls = url_input.split(",")

# Run the app
if __name__ == "__main__":
    main()