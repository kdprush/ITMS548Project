import requests
import tkinter as tk
from tkinter import ttk

api_key = #INSERT API KEY HERE WITH "APIKEY"
url = "https://serpapi.com/search"

params = {
    "engine": "google",
    "q": "Chicago crime",
    "num": 15,
    "api_key": api_key
}

response = requests.get(url, params=params)
data = response.json()

root = tk.Tk()
root.title("Chicago Crime Search Results")

table_data = []

for result in data['organic_results']:
    title = result['title']
    link = result['link']
    table_data.append([title, link])

tree = ttk.Treeview(root, columns=('Title', 'URL'), show='headings')
tree.heading('Title', text='Title')
tree.heading('URL', text='URL')

for row in table_data:
    tree.insert('', 'end', values=row)

tree.pack(fill='both', expand=True)

root.mainloop()