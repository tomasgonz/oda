import os
import urllib
import pandas as pd
import time

def download_file(url, file_name):
    url = "https://datasource.nyc3.digitaloceanspaces.com/" + file_name
    try:
        urllib.request.urlretrieve(url, "data/" + file_name)
    except:
        print("Error downloading file. Please try again later.")

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
        while not os.path.isfile("data/" + file_name):
            time.sleep(1)
        return pd.read_csv(file_name)