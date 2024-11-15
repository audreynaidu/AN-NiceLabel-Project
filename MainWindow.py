# Import Module
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk
import ArenaAPI
import FileHelperFunctions

root = ctk.CTk()
 
ARENA_SESSION_ID= ''

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("green")   
appWidth, appHeight = 600, 700


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x600")
        self.attributes('-topmost', 1)

        self.label = ctk.CTkLabel(self, text="Label Information: ")
        self.label.pack(padx=20, pady=20)

        self.text_area = ctk.CTkTextbox(self,
                                         width=300,
                                         height=400)
        self.text_area.pack(expand=True, padx=20, pady=20, fill=BOTH, anchor = CENTER)
        self.display_file_contents()

    def display_file_contents(self):
        file_path = app.get_cur_filename()

        if(file_path != "" or file_path != None):
            try:
                with open(file_path, 'r') as file:
                    contents = file.read()
                    self.text_area.delete("1.0", "end")
                    self.text_area.insert("0.0", contents, "center")
            except Exception:
                print("error opening file")
                self.text_area.insert("0.0", f"Error opening file", "center")
                
        else:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("0.0", f"Nothing to display.", "center")
            
            

class ArenaProcessor(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Nice Label Application")
        self.geometry(f"{appWidth}x{appHeight}")
        global arena_api; arena_api = ArenaAPI.ArenaAPI()
        arena_api.login()
        print("logged in: " + arena_api.arena_session_id)

        self.export_all_labels = ctk.BooleanVar()

        # all widgets will be here
        # adding a label to the root window
        self.enter_part_number = ctk.CTkLabel(self, 
                            text = "Enter Part Number: ")
        self.enter_part_number.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")
        # adding Entry Field
        self.part_entry = ctk.CTkEntry(self, width=200,
                            placeholder_text="EN-WS-ZC3-ZB-IV")
        self.part_entry.grid(row=0, column=1,
                            columnspan=3, padx=20,
                            pady=20, sticky="ew")
        
        self.displayBox = ctk.CTkTextbox(self,
                                         width=200,
                                         height=100)
        self.displayBox.grid(row=3, column=0,
                             columnspan=4, padx=20,
                             pady=20, sticky="nsew")
        
        # button widget with red color text
        # inside
        self.part_entry.bind('<Return>', self.entered_part_number)
        self.submit_button = ctk.CTkButton(self, text = "Submit" , fg_color="red", command=self.clicked)
        # Set Button Grid
        self.submit_button.grid(row=2, column=1,
                                        columnspan=2, padx=20, 
                                        pady=20, sticky="ew")

        self.toplevel_window = None

        self.display_results_button = ctk.CTkButton(self,
                                         text="Display Most Recent Label Information", state=ctk.DISABLED,
                                         command=self.open_file_display)
        self.display_results_button.grid(row=4, column=1,
                                        columnspan=2, padx=20, 
                                        pady=20, sticky="ew")

        self.export_to_excel_button = ctk.CTkButton(self,
                                         text="Export to Excel", state=ctk.DISABLED,
                                         command=self.export_to_excel)
        self.export_to_excel_button.grid(row=5, column=1,
                                        columnspan=2, padx=20, 
                                        pady=20, sticky="ew")
        self.export_all_labels_checkbox = ctk.CTkCheckBox(self, text="Export All Searched Labels", 
                                        variable=self.export_all_labels)
        # Pack the checkbox widget, adding padding around it
        self.export_all_labels_checkbox.grid(row=5, column=3, padx=10, pady=10)
        

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def export_all_labels_checked(self):
        if self.export_all_labels.get() == 'true':
            self.export_all_labels.set('false')
        else:
            self.export_all_labels.set('true')
    
    def open_file_display(self):
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()  # if window exists focus it

    def get_cur_filename(self):
        return self.cur_filename
    
    def entered_part_number(self, event):
        self.clicked()
    
    def clicked(self):
        self.displayBox.delete("1.0", "end")
        res = self.part_entry.get().strip()
        if(res == None or res == ""):
            self.displayBox.insert("0.0", "Please enter a part number.")
            self.display_results_button.configure(state = ctk.DISABLED)
        else:
            
            try:
                cur_filename = arena_api.arena_run(res)
                if cur_filename == 'Invalid.txt':
                    raise Exception
                self.cur_filename = cur_filename
                self.displayBox.insert("0.0", "Part Number(s): " + res)
                self.display_results_button.configure(state = ctk.NORMAL)
                self.export_to_excel_button.configure(state = ctk.NORMAL)

            except Exception:
                self.displayBox.insert("0.0", "The part number you entered was invalid.")
                self.display_results_button.configure(state = ctk.DISABLED)
                
    
    def export_to_excel(self):
        arena_api.write_label_to_file(self.export_all_labels.get())
        print('Wrote to file successfully')
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            arena_api.logout()
            FileHelperFunctions.delete_all_files_in_folder('./Item_Attributes/')
            self.quit()
            self.destroy()

        

def openNewWindow():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = ctk.CTkToplevel(app)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("200x200")
 
    # A Label widget to show in toplevel
    ctk.CTkLabel(newWindow, 
          text ="This is a new window").pack()






if __name__ == "__main__":
    
    app = ArenaProcessor()
    # Used to run the application
    app.mainloop() 
    
    