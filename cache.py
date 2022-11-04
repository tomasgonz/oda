import os
import requests
import pandas as pd
import time
from tqdm import tqdm

def download_file(url, file_name):
    url = "https://datasource.nyc3.digitaloceanspaces.com/oecd/" + file_name
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 8096
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with response as r:
            r.raise_for_status()
            with open('data/' + file_name, 'wb') as f:
                for chunk in r.iter_content(block_size):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
            
            r.close()
        
        progress_bar.close()
    
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
        return pd.read_csv("data/" + file_name)