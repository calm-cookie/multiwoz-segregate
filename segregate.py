''' 
Program purpose: Segregate the MultiWoz 2.1 Dataset into 'attraction', 'restaurant', 'taxi' and a combination of these domains

Input: MultiWoz 2.1 Dataset in JSON

Output:
1. JSON files separated into different folders
2. stats.xlsx with count of number of files
3. list.json in each folder with list of filenames

Running command syntax:
1. Set the OUTPUT_DIR and DATASET paths in the file (line 20, 21)
2. Install xlswriter using 'pip3 install xlsxwriter'
3. Run using 'python3 segregate.py'
'''
import os
import json
import xlsxwriter

OUTPUT_DIR = './' # Set the output directory relative to the directory in which file is present
DATASET = './data.json'   # Set the path of dataset (relative to the directory in which file is present)

# DO NOT CHANGE ANYTHING AFTER THIS LINE
# --- Setting location of the parent directory  ---
parent_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(parent_dir, OUTPUT_DIR)

directories = {
    'attraction': 0,
    'restaurant': 0,
    'taxi': 0,
    'attraction-restaurant': 0,
    'attraction-taxi': 0,
    'restaurant-taxi': 0,
    'attraction-restaurant-taxi': 0
}

def create_directories(parent_dir, directories):
    '''
    1. Create folders for each domain
    2. Create a blank list.json in each folder
    '''
    print("Creating directories...\n")
    
    for directory in directories:
        # --- Create empty folders for each domain ----
        path = os.path.join(parent_dir, 'dataset/' + directory)
        
        try:
            os.makedirs(path)
            print("Created -> {}".format(path))
        
        except FileExistsError as exists:
            print("Already exists -> {}".format(exists.filename))

        # --- Initiate a blank list.json in each folder to store the list of filenames ---
        path = os.path.join(parent_dir, 'dataset/' + directory + '/list.json')
        with open(path, 'w') as f:
            json.dump([], f, indent=2)

    print("Directories created :)")


def separate_file(data, parent_dir, combination, filename):
    '''
    1. Create a separate JSON file with data in the apt folder
    2. Add 1 to the domain count
    3. Add filename of JSON to list.json
    '''
    # --- Create a new file ---
    path = os.path.join(parent_dir, 'dataset/{}/{}'.format(combination, filename))
    with open(path, 'w') as f:
        json.dump(data[filename], f, indent=2)

    # --- Update the domain count ---
    directories[combination] += 1

    # --- Set path for list.json ---
    path = os.path.join(parent_dir, 'dataset/{}/list.json'.format(combination))

    # --- Read list.json and add new filename to the list.json ---
    with open(path, 'r') as f:
        files = json.load(f)
        files.append(filename)

    # --- Write the new filename to list.json
    with open(path, 'w') as f:
        json.dump(files, f, indent=4)

def write_to_excel(parent_dir):
    '''
    Write the stats stored in 'directories' global variable to excel file
    '''
    print("\nWriting to excel...")
    wb = xlsxwriter.Workbook(os.path.join(parent_dir, 'dataset/stats.xlsx'))
    sheet = wb.add_worksheet('stats') 
    
    row = 1
    sheet.write(0, 0, "Domain")
    sheet.write(0, 1, "Number of files")
    for directory in directories:
        sheet.write(row, 0, directory)
        sheet.write(row, 1, directories[directory])
        row += 1 
    
    wb.close()
    print("Written :)")

def segregate(dataset, parent_dir):
    '''
    Iterate over the complete dataset to segrate into different files
    '''
    # --- Open dataset file and decode it ---
    try:
        f = open(dataset)
        data = json.load(f)

    except FileNotFoundError:
        return print("No such file {}".format(dataset))

    except json.decoder.JSONDecodeError:
        return print("The file {} cannot be decoded as JSON".format(dataset))
    
    print("\nSegregating...")
    print("This might take a couple of mintures")
    # --- Iterate over the original dataset and perform checks ---
    for filename in data:
        goal = data[filename]['goal']

        if not (goal['police'] or goal['train'] or goal['hospital'] or goal['hotel']):

            if goal['attraction'] and goal['restaurant'] and goal['taxi']:
                separate_file(data, parent_dir, 'attraction-restaurant-taxi', filename)

            elif goal['attraction'] and goal['restaurant']:
                separate_file(data, parent_dir, 'attraction-restaurant', filename)

            elif goal['restaurant'] and goal['taxi']:
                separate_file(data, parent_dir, 'restaurant-taxi', filename)

            elif goal['attraction'] and goal['taxi']:
                separate_file(data, parent_dir, 'attraction-taxi', filename)

            elif goal['attraction']:
                separate_file(data, parent_dir, 'attraction', filename)
            
            elif goal['restaurant']:
                separate_file(data, parent_dir, 'restaurant', filename)

            elif goal['taxi']:
                separate_file(data, parent_dir, 'taxi', filename)

    # --- Close dataset file --- 
    f.close()
    print("Done :)")

create_directories(parent_dir, directories)
segregate(DATASET, parent_dir)
write_to_excel(parent_dir)