import os  # for file content operations
import json  # for pretty-printing responses
import requests  # for GET, PUT, POST, DELETE
import requests_toolbelt  # for creating multipart file resources with content
import traceback
import FileHelperFunctions
import ArenaHelperFunctions
from datetime import datetime


#bcs_production = 896614515
#bcs_sandbox = 900467460 

class ArenaSampleError(Exception):
        """ Exception in Arena sample functions. """
        pass

class ArenaAPI:
    
    def __init__(self):
        try: 
            with open('ArenaLogin/credentials.txt', 'r') as f:
                self.email = f.readline().strip()
                self.password = f.readline().strip()
                self.workspace_id = (int)(f.readline().strip())
        except Exception:
            print("error reading credentials.txt")
        self.URL = 'https://api.arenasolutions.com/v1'
        self.item_nums_searched = []
        self.labels_list = []
        self.item_attribute_skeleton = {
            'PartNumber': '',
            'name' : '',
            'guid' : '',
            'UnitUPC' : '',
            'IntermediateUPC' : '',
            'MasterCartonUPC' : '',
            'BusinessUnit' : '',
            'CountryOfOrigin' : '',
            'IntermediateQty' : '',
            'MasterCartonQty' : '',
            'LabelTextENG1' : '',
            'LabelTextENG2' : '',
            'LabelTextSPN1' : '',
            'LabelTextSPN2' : '',
            'LabelTextFRN1' : '',
            'LabelTextFRN2' : '',
            'ColorENG' : '',
            'ColorSPN' : '',
            'ColorFRN' : '',
            'CatalogNumber' : '',
            'MFGLocation' : '',
            'UnitAgilePN': '',
            'IntermediateAgilePN': '',
            'MasterAgilePN': '',
        }

    
    def login(self):
        """
        Login to Arena.

        :param url: URL to Arena API
        :param credentials: dictionary of credentials like:
            credentials = {
                'email': 'joe.cool@arenasolutions.com',
                'password': 'joes_password',
                'workspaceId': 12345678,
            }
        :return: Arena session id
        """
        endpoint = self.URL + '/login'
        headers = {
            'content-type': 'application/json',
        }
        credentials = {'email': self.email, 'password': self.password, 'workspaceId': self.workspace_id, 'Arena-Usage-Reason': 'legrand VSCode / 1.18 testing API',}
        response = requests.post(endpoint, headers=headers, json=credentials)
        response_body = response.json()

        if response.status_code == 200:  # success
            self.arena_session_id = response_body['arenaSessionId']
            return response_body
        else:  # error
            raise ArenaSampleError(response_body['errors'])


    def logout(self):
        """
        Logout of Arena.

        :param url: URL to Arena API
        :param session_id: Arena session id
        :return: None
        """
        endpoint = self.URL + '/logout'
        headers = {
            'content-type': 'application/json',
            'arena_session_id': self.arena_session_id,
        }
        response = requests.put(endpoint, headers=headers)

        if response.status_code == 200:  # success
            print('>>> Logout')
            return None  # no content to return
        else:  # error
            response_body = response.json()  # get the error messages
            raise ArenaSampleError(response_body['errors'])
        
    def print_by_line(response):
        for keys,values in response.items():
            print(str(keys) + ": "  + str(values))


    def dump_guid_to_file(self, headers, filename):
        endpoint = self.URL + '/settings/items/categories/'
        try:
            response = requests.get(endpoint, headers=headers)
            response_body = response.json()
            with open(filename +'.json', 'w') as f:
                json.dump(response_body, f, indent=4)
            print("Dumped to " + filename + ".json successfully")
        except Exception:
            print("error dumping to file")
            traceback.print_exc()

        
    def get_item_guid(self, headers, item_number):
        params = {
            'number': item_number
        }
        try:
            response = requests.get(self.URL + '/items', headers=headers, params=params)
            response_data = response.json()
            item_guid = (response_data.get('results'))[0]['guid']
            print("item guid: " + item_guid)
            return item_guid
        except Exception:
            print("Error getting data from " + item_number)
            traceback.print_exc()
            return ''

    def check_duplicate_item(self, item_num):
        if item_num in self.item_nums_searched:
            self.recent_index = self.item_nums_searched.index(item_num)
            print('duplicate item')
            return True
        return False

    def get_item_attributes(self, headers, item_num, item_guid, item_attributes_skeleton):
        filename = item_num + '_info'
        filename = filename.replace(' ', '')
        if self.check_duplicate_item(item_num):
            print('got to check duplicate item part')
            return 'Item_Attributes/Attributes_' + filename
        item_attributes = item_attributes_skeleton.copy()
        endpoint = self.URL + '/items/' + item_guid
        try:
            print('getting item info')
            response = requests.get(endpoint, headers=headers)
            response_data = response.json()
             
            item_attributes['PartNumber'] = item_num
            item_attributes['name'] = response_data.get('name')
            item_attributes['guid'] = item_guid
            for item in response_data['additionalAttributes']:
                if(item['name']== "Business Unit"):
                    item_attributes['BusinessUnit']= item.get('value')
                elif(item['name'] == "UPC Code - Unit (B)"):
                    item_attributes['UnitUPC']= item.get('value')
                elif(item['name'] == "UPC Code - Intermediate Package (B1)"):
                    item_attributes['IntermediateUPC']= item.get('value')
                elif(item['name'] == "UPC Code - Master carton (B2)"):
                    item_attributes['MasterCartonUPC']= item.get('value')
                elif(item['name'] == "Country of Origin"):
                    item_attributes['CountryOfOrigin']= item.get('value')
                elif(item['name'] == "Intermediate quantity"):
                    item_attributes['IntermediateQty']= item.get('value')
                elif(item['name'] == "Master Carton Quantity"):
                    item_attributes['MasterCartonQty']= item.get('value')
                elif(item['name'] == "Label Text Line 1 (EN)"):
                    item_attributes['LabelTextENG1']= item.get('value')
                elif(item['name'] == "Label Text Line 2 (EN)"):
                    item_attributes['LabelTextENG2']= item.get('value')
                elif(item['name'] == "Label Text Line 1 (SP)"):
                    item_attributes['LabelTextSPN1']= item.get('value')
                elif(item['name'] == "Label Text Line 2 (SP)"):
                    item_attributes['LabelTextSPN2']= item.get('value')
                elif(item['name'] == "Label Text Line 1 (FR)"):
                    item_attributes['LabelTextFRN1']= item.get('value')
                elif(item['name'] == "Label Text Line 2 (FR)"):
                    item_attributes['LabelTextFRN2']= item.get('value')
                elif(item['name'] == "Label Color (EN)"):
                    item_attributes['ColorENG']= item.get('value')
                elif(item['name'] == "Label Color (SP)"):
                    item_attributes['ColorSPN']= item.get('value')
                elif(item['name'] == "Label Color (FR)"):
                    item_attributes['ColorFRN']= item.get('value')
                elif(item['name'] == "Catalog Number"):
                    item_attributes['CatalogNumber']= item.get('value')
                elif(item['name'] == "Manufacturing Location"):
                    item_attributes['MFGLocation']= item.get('value')
            
            item_attributes['CountryOfOrigin'] = "Made in " + ArenaHelperFunctions.get_full_country_name(item_attributes['CountryOfOrigin'])
            if(item_attributes['MFGLocation'] == 'Creation'):
                item_attributes['MFGLocation'] = "Vaughan ON"
            if(item_attributes['MFGLocation'] == '' or item_attributes['MFGLocation'] == None ):
                item_attributes['MFGLocation'] = "Carlsbad, CA"
            if(item_attributes['IntermediateQty']== ''):
                item_attributes['IntermediateQty'] = '0'
            if(item_attributes['MasterCartonQty']== ''):
                item_attributes['MasterCartonQty'] = '0'
            
            item_attributes['Graphics'] = item_num + '.pdf'
            unit_agile = self.search_unit_PN(headers, item_num)
            if unit_agile == None or unit_agile == '':
                item_attributes['UnitAgilePN'] = 'Unable to Find'
            else:
                item_attributes['UnitAgilePN'] =  unit_agile

            intermediate_agile = self.search_intermediate_PN(headers, item_num)
            if intermediate_agile == None or intermediate_agile == '':
                item_attributes['IntermediateAgilePN'] = 'Unable to Find'
            else:
                item_attributes['IntermediateAgilePN'] =  intermediate_agile

            master_agile = self.search_master_PN(headers, item_num)
            if master_agile == None or master_agile == '':
                item_attributes['MasterAgilePN'] = 'Unable to Find'
            else:
                item_attributes['MasterAgilePN'] =  master_agile
                   
            FileHelperFunctions.dump_dict_to_file('Item_Attributes/Attributes_' + filename, item_attributes)
            self.labels_list.append(item_attributes)
            self.item_nums_searched.append(item_num)
            self.recent_index = -1
            return 'Item_Attributes/Attributes_' + filename
        except Exception:
            print("Error getting data from " + item_guid)
            traceback.print_exc()
            return None
        
    def generate_label_headers(self):
        row = []
        for key in self.item_attribute_skeleton:
            row.append(key)
        return row
    def generate_label_row(self, label):
        cur_row = []
        for key in label:
            cur_row.append(label[key] if label[key] !='' else 'None')
        return cur_row
    def generate_label_rows(self, export_all_labels):
        rows = []
        if not export_all_labels:
            rows.append(self.generate_label_row(self.labels_list[self.recent_index]))
        else:
            for label in self.labels_list:
                rows.append(self.generate_label_row(label))
        return rows

    def write_label_to_file(self, export_all_labels):
        print("Export all labels: " + str(export_all_labels))
        headers = self.generate_label_headers()
        label_content = self.generate_label_rows(export_all_labels)
        part_num = self.labels_list[self.recent_index]['PartNumber']
        if export_all_labels:
            current_datetime = (datetime.now())
            current_datetime = str(current_datetime.replace(microsecond=0))
            current_datetime = current_datetime.replace(' ', '_')
            current_datetime = current_datetime.replace(':', '-')
            filename = current_datetime
        else: 
            filename = part_num

        
        
        FileHelperFunctions.dump_contents_to_csv('Label_CSV/' + filename + '.csv', headers, label_content)

    def search_unit_PN(self, headers, item_num):
        #unit:"LABEL PKG CATALOG# TRI-LIN BOX"
        #/&category.guid=L3N6B1RQ3VEN6P56U3XU
        name = "LABEL PKG " + item_num + " TRI-LIN BOX"
        endpoint = self.URL + '/items?name=*'+ item_num
        try:
            response = requests.get(endpoint, headers=headers)
            response_body = response.json()
            results = response_body.get('results')
            for dict in results: 
                if "LABEL PKG " + item_num + " TRI-LIN BOX" in dict.get("name"):
                    print(name + " found.")
                    if dict.get('revisionNumber') == None or dict.get('revisionNumber') =='':
                        revision = ' '
                    else:
                        revision = ' r' + dict.get('revisionNumber')
                
                    return dict.get("number") + revision
            print(name + " not found.")
            return None
        except Exception:
            print("Error getting data from " + name)
            traceback.print_exc()
    
    def search_intermediate_PN(self, headers, item_num):
        #/&category.guid=L3N6B1RQ3VEN6P56U3XU
        name = "LABEL PKG " + item_num + " TRI-LIN INR"
        endpoint = self.URL + '/items?name=*'+ item_num
        try:
            response = requests.get(endpoint, headers=headers)
            response_body = response.json()
            results = response_body.get('results')
            for dict in results: 
                if "LABEL PKG " + item_num + " TRI-LIN INR" in dict.get("name"):
                    print(name + " found.")
                    if dict.get('revisionNumber') == None or dict.get('revisionNumber') =='':
                        revision = ' '
                    else:
                        revision = ' r' + dict.get('revisionNumber')
                
                    return dict.get("number") + revision
            print(name + " not found.")
            return None
        except Exception:
            print("Error getting data from " + name)
            traceback.print_exc()

    def search_master_PN(self, headers, item_num):
        #master: "LABEL PKG CATALOG# TRI-LIN SHIP"
        #/&category.guid=L3N6B1RQ3VEN6P56U3XU
        name = "LABEL PKG " + item_num + " TRI-LIN SHIP"
        endpoint = self.URL + '/items?name=*'+ item_num
        try:
            response = requests.get(endpoint, headers=headers)
            response_body = response.json()
            results = response_body.get('results')
            for dict in results:
                if "LABEL PKG " + item_num + " TRI-LIN SHIP" in dict.get("name"):
                    print(name + " found.")
                    if dict.get('revisionNumber') == None or dict.get('revisionNumber') =='':
                        revision = ' '
                    else:
                        revision = ' r' + dict.get('revisionNumber')
                
                    return dict.get("number") + revision
            print(name + " not found.")
            return None
        except Exception:
            print("Error getting data from " + name)
            traceback.print_exc()
    
 


    def arena_run(self, item_nums):
        headers = {
            'content-type': 'application/json',
            'arena_session_id': self.arena_session_id
        }
        item_nums = item_nums.strip()
        file_path = ''
        search_list = []
        item_nums = item_nums.replace(" ", "")
        if ',' in item_nums:
            search_list = item_nums.split(',')
        else:
            search_list = [item_nums]
        invalid_count = 0
        for item_num in search_list:
            if(item_num == 'sample'):
                item_num = 'EN-WS-SC3-CBK-WH'
            item_guid = self.get_item_guid(headers, item_num)
            if item_guid == None or item_guid == '':
                invalid_count = invalid_count + 1
                print('unable to get data on ' + item_num)
            else:
                file_path = self.get_item_attributes(headers, item_num, item_guid, self.item_attribute_skeleton)
                if file_path == None or file_path == '':
                    invalid_count = invalid_count + 1
                    print('unable to create file for ' + item_num)
        if invalid_count == len(search_list):
            return 'Invalid.txt'
        return file_path + ".txt"