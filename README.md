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
3. Run with Editor: To run the program through an editor like VS_Code, open the MainWindow.py file located in the root directory and run it. 
3. Run with Terminal: To run the program through a terminal, navigate to the root directory within the terminal and run the command: python MainWindow.py
4. Exiting the program: Use the X button on top of the main window to exit.
   **Important:** Please try to avoid force quitting the program (Ctr+C) unless absolutely necessary and only close the program with the exit button to ensure that you are properly logged out of Arena.

# Usage
# Searching
With the popup open, enter any part number and it will search the Arena database for the attributes of that part. If the part number is invalid, the text-box will state that. If it is valid, it will print out the part number you typed. You can display the information of the most recent part number you searched by clicking the display labels button or export the attributes to a .csv file by clicking the export button. When exporting, you can also select the option to export all the part numbers you have searched in that session. 

The .csv files are located in the Label_CSV folder.
When exporting all part number attributes, the file format will be:
  current day and time: YYYY-MM-DD_HH-MM-SS.csv
When exporting just one part number's attributes, the file format will be:
  part-number.csv

# Features
- Multiple Labels can be searched at the same time. Separate each part number to be searched with a comma.
- If a part number within multiple searches at once is invalid, the other valid part numbers will still be searched and added to the list of searched labels.
- Includes a duplicate detection feature where duplicate searches within one session will not be added to the part list to avoid duplicate part attributes when exporting all searched labels.
- The Item_Attributes directory exists to help with the display labels feature and all text files generated during the session will be deleted upon closure of the application.

# Contact
Audrey Naidu: audrey.naidu@legrand.com

