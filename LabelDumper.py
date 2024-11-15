import os  # for file content operations
import json  # for pretty-printing responses
import requests  # for GET, PUT, POST, DELETE
import requests_toolbelt  # for creating multipart file resources with content
import traceback
import FileHelperFunctions
import ArenaAPI
import ArenaHelperFunctions

def get_applicable_labels(arena_api, headers, params):
    response = requests.get('https://api.arenasolutions.com/v1/items?O6Q9E4UT6YFXGZEHCC1E=*&category.guid=0I2LQG65IAT3M5HO1ZUR&limit=200', headers=headers, params=params)
    #https://api.arenasolutions.com/v1/items?O6Q9E4UT6YFXGZEHCC1E=label_color_EN&category.guid=0I2LQG65IAT3M5HO1ZUR
    #working link: https://api.arenasolutions.com/v1/items?O6Q9E4UT6YFXGZEHCC1E=*&limit=50
    applicable_labels = response.json()
    label_numbers = []
    for label in applicable_labels['results']:
        label_numbers.append(label.get('number'))
    FileHelperFunctions.dump_results_to_file('Part_Numbers_Applicable_Labels_Color', label_numbers)
    print("Labels retrieved Successfully")


if __name__ == '__main__':
    arena_api = ArenaAPI.ArenaAPI()
    login_response = arena_api.login()
    headers = {
            'content-type': 'application/json',
            'arena_session_id': arena_api.arena_session_id
    }
    params = {
        'lifecyclePhase.guid': 'J1L49ZPO1TBEXGZI0RB4'
    }
    get_applicable_labels(arena_api, headers, params)
    arena_api.logout()
        