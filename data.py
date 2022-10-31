from cache import load_file
def get_oda_recipients():    
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/DACGEO.csv", "DACGEO.csv")

def get_oda_volume(): 
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/TABLE1_export.csv", "TABLE1_export.csv")

def get_oda_sectors(): 
    return load_file("https://datasource.nyc3.digitaloceanspaces.com/TABLE5_export.csv", "TABLE5_export.csv")
