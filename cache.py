import os
import urllib

def download_file(url, file_name):
    st.write("Downloading data. Please, be patient... it is a lot of data...")
    url = "https://datasource.nyc3.digitaloceanspaces.com/"
    
    urllib.request.urlretrieve(url, file_name)

def check_if_file_exists(url, file_name):
    if os.path.isfile(file_name):
        return True
    else:
        download_file(url, file_name)
        return False

