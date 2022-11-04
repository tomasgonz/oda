from cache import load_file

def get_oda_recipients():    
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/oecd/DACGEO.csv", "DACGEO.csv")

def get_oda_volume(): 
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/oecd/TABLE1_export.csv", "TABLE1_export.csv")

def get_oda_sectors(): 
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/oecd/TABLE5_export.csv", "TABLE5_export.csv")

def get_crs():
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/oecd/CRS2020data.csv", "CRS2020data.csv")
