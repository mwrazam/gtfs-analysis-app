import DBTools.DBConnector as DBH
import Agency
import sys, csv, os, zipfile
import wget

def load_agencies_from_csv(filename):
    agencies = []
    fp = f"{sys.path[0]}/Data/{filename}"
    with open(fp, 'r') as agency_file:
        for line in csv.DictReader(agency_file):
            agencies.append(line)
    return agencies

def load_agency_static_data(agency, reload=False):
    static_data = {}
    if reload:
        # deal with wiping static agency files and reloading them
        pass
    if not check_static_data_exists(agency):
        # if we don't have static files, get them
        print(f"{agency['agency_name']} does not have static data files")
        download_agency_static_data(agency, reload=False, auto_extract=True)

    files = get_static_file_list(agency)
    f_dir = f"{sys.path[0]}/Data/{agency['agency_name']}/static"
    print(f"Loading static data for {agency['agency_name']}, this may take a few minutes...")
    for f in files:
        static_data[f] = {'cols': [], 'data': [[]]}
        with open(f"{f_dir}/{f}.txt", 'r') as static_file:
            data = []
            for line in csv.reader(static_file):
                data.append(line)
            if len(data) > 0:
                static_data[f]['cols'] = data[0]
            if len(data) > 1:
                static_data[f]['data'] = data[1:]
            
    return static_data

def extract_agency_static_data(zip_filename, extract_location):
    if not os.path.exists(extract_location):
        os.makedirs(extract_location)

    print("Extracting files...")
    with zipfile.ZipFile(zip_filename, 'r') as file:
        print(f"Extracting {zip_filename} to {extract_location}")
        file.extractall(extract_location)

def download_agency_static_data(agency, reload=False, auto_extract=True):
    filename = f"{sys.path[0]}/Data/static_zips/{agency['agency_name']}.zip"
    if reload and os.path.exists(filename):
        os.remove(filename)

    if os.path.exists(filename):
        print(f"Static zip file already exists for {agency['agency_name']}")
    else:
        try:
            print(f"Downloading file from... {agency['static']}")
            wget.download(agency['static'], filename)
        except:
            print(f"Could not download file...")

    if auto_extract:
        extract_to = f"{sys.path[0]}/Data/{agency['agency_name']}/static"
        extract_agency_static_data(filename, extract_to)

# check static data files
def check_static_data_exists(agency):
    # for now, this will only check if the folder exists
    fp = None
    if agency['static_format'] == 'zip':
        fp = f"{sys.path[0]}/Data/{agency['agency_name']}/static"
    return os.path.exists(fp)

def get_static_file_list(agency):
    if check_static_data_exists(agency):
        filenames = set()
        fp = f"{sys.path[0]}/Data/{agency['agency_name']}/static"
        for file in os.listdir(fp):
            if file.endswith(".txt"):
                filenames.add(file.split(".")[0])
        return filenames
    return False

def cast_static_data(static_data):
    pass

def run():
    dbc = DBH.DBConnector(host="localhost", user="postgres", password="1234", database="postgres")
    dbc.connect()

    print(f"{'*'*100}")

    #agencies = load_agencies_from_csv("GTFS-FEEDS.csv")
    #dbc.sync_agencies(agencies, reload=False)
    #agencies = dbc.get_agencies(active=True)
    #for agency in agencies:
    #    load_agency_static_data(agency)

    #dbc.build_static_samples_tables(reload=True)

    agencies = dbc.get_agencies(active=True)
    for agency in agencies:
        #tables = get_static_file_list(agency)
        #dbc.create_static_templates_for_agency(agency['agency_name'], tables, reload=True)
        
        static_data = load_agency_static_data(agency, reload=False)
        dbc.sync_static_tables_for_agency(agency['agency_name'], static_data, reload=True)
        #print(static_data.keys())

        
        #data_types = get_table_columns
        #dbc.sync_static_tables_for_agency(agency['agency_name'], static_data, reload=False)

    dbc.disconnect()
            
if __name__ == '__main__':
    run()