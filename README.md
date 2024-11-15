# AN-NiceLabel-Project
NiceLabel project for automating label creation for Legrand

# Author
Audrey Naidu

# Requirements
Python: https://www.python.org/downloads/
VS_Code(Optional): https://code.visualstudio.com/download

# Setup
1. After cloning the repository, and installing the requirements, go to the ArenaLogin directory and input your Arena credentials and workspace ID into credentials.txt as per the instructions.
2. Navigate to the root directory where MainWindow.py is located. 
   **Important:** If you are not in the root directory, the program will throw an error upon running.
4. Run with Editor: To run the program through an editor like VS_Code, open the MainWindow.py file located in the root directory and run it. 
3. Run with Terminal: To run the program through a terminal, navigate to the root directory within the terminal and run the command: python MainWindow.py

# Usage
# Searching
With the popup open, enter any part number and it will search the Arena database for the attributes of that part. If the part number is invalid, the text-box will state that. If it is valid, it will print out the part number you typed. You can display the information of the most recent part number you searched or export the attributes to a .csv file. When exporting, you can also select the option to export all the part numbers you have searched in that session. 

The .csv files are located in the Label_CSV folder.

# Features
Multiple Labels can be searched at the same time. Separate each part number to be searched with a comma.
If a part number within multiple searches at once is invalid, the other valid part numbers will still be searched and added to the list of searched labels.

# Contact
Audrey Naidu: audrey.naidu@legrand.com

