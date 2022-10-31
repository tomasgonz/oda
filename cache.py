import os
import urllib
import pandas as pd

def download_file(url, file_name):
    url = "https://datasource.nyc3.digitaloceanspaces.com/" + file_name
    
    urllib.request.urlretrieve(url, "data/" + file_name)

def check_if_file_exists(url, file_name):
    os.makedirs("data") if not os.path.isdir("data") else None
            
    if os.path.isfile("data/" + file_name):
        return True
    else:
        download_file(url, file_name)
        return False

def load_file(url, file_name):
    if check_if_file_exists(url, file_name):        
        return pd.read_csv("data/" + file_name)
    else:
        download_file(url, file_name)        
        return pd.read_csv(file_name)
