import os  # for file content operations
import json  # for pretty-printing responses
import requests  # for GET, PUT, POST, DELETE
import requests_toolbelt  # for creating multipart file resources with content
import traceback 
import ArenaAPI
import csv
import shutil

def dump_dict_to_file(filename, dict):
    with open(filename + '.txt', 'w') as f:
        for key in dict:
            f.write(key + ': ' + str(dict.get(key)) + '\n')
    print("dumped to " + filename + " successfully")



def dump_results_to_file(filename, results):
    try:
        with open(filename +'.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("Dumped to " + filename + ".json successfully")
    except Exception:
        print("error dumping to file")
        traceback.print_exc()


def dump_contents_to_csv(filename, header, content):
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            if content != None or content != []:
                writer.writerows(content)
    except Exception:
        print("Error writing to " + filename)
        traceback.print_exc()

def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            print(f"Failed to delete {file_path}: {e}")