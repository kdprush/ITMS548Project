import tkinter as tk
from tkinter import ttk
import requests
import webbrowser

def fetch_crime_data():
    """
    Function to fetch crime data from the Chicago data portal.
    Returns:
        List: A list of dictionaries containing crime data.
    """
    # API endpoint for Chicago crime data
    url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"

    # Parameters to limit the data to the 1000 most recent entries and order by ID descending
    params = {"$limit": 1000, "$order": ":id DESC"}

    # Fetching data from the API
    response = requests.get(url, params=params)

    # Checking if the request was successful and returning data accordingly
    return response.json() if response.status_code == 200 else []

def create_gui():
    """
    Function to create the GUI for displaying crime data.
    """
    def update_data():
        """
        Function to update the displayed crime data.
        """
        # Fetching new crime data
        new_data = fetch_crime_data()

        # Clearing the treeview
        tree.delete(*tree.get_children())

        # Inserting the new crime data into the treeview
        for i, record in enumerate(new_data, start=1):
            tree.insert("", "end", values=(
                record["case_number"],
                record["id"],
                record["date"].split("T")[0],
                record["date"].split("T")[1],
                f"{record['block']}, {record['district']}",
                "Yes" if record["arrest"] else "No",
                record["primary_type"]
            ))

    def open_chicago_map():
        """
        Function to open the City of Chicago's Crime Map in the default web browser.
        """ 
        crime_map_url = "https://data.cityofchicago.org/Public-Safety/Crimes-Map/dfnk-7re6"
        webbrowser.open(crime_map_url)      

    # Creating the main window
    root = tk.Tk()
    root.title("Chicago Crime Data")

    # Making the window resizable
    root.resizable(True, True)

    # Set window size to half the screen size
    screen_width = root.winfo_screenwidth() // 2
    screen_height = root.winfo_screenheight() // 2
    root.geometry(f"{screen_width}x{screen_height}")

    # Adding a scrollbar to the root window
    scrollbar = ttk.Scrollbar(root, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Creating a treeview widget to display crime data
    tree = ttk.Treeview(root, columns=("Case Number", "Crime ID", "Date", "Time", "Location", "Arrest", "Crime Type"), yscrollcommand=scrollbar.set, show="headings")
    tree.heading("Case Number", text="Case Number")
    tree.heading("Crime ID", text="Crime ID")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Location", text="Location")
    tree.heading("Arrest", text="Arrest")
    tree.heading("Crime Type", text="Crime Type")
    tree.pack(fill="both", expand=True)

    # Linking scrollbar to treeview
    scrollbar.config(command=tree.yview)

    # Adding an update button
    update_button = tk.Button(root, text="Update", command=update_data, width=10, height=2)
    update_button.pack()

    # Adding a button to open the Chicago map
    map_button = tk.Button(root, text="Open Chicago Map", command=open_chicago_map, width=20, height=2)
    map_button.pack()

    # Set window to appear in front of other tasks
    root.attributes("-topmost", True)

    # Function to populate the treeview with data on startup
    update_data()

    # Running the main event loop
    root.mainloop()

if __name__ == "__main__":
    # Calling the function to create the GUI
    create_gui()


