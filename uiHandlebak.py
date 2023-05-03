import tkinter as tk
from tkinter import ttk
from ttkwidgets import checkboxtreeview as checktree


import threading
from pkHandle import  *
# import win32com.client
from stockHandle import *

global added_items

added_items = []
kospistock, kosdaqstock = getStockList()




# create the main window
root = tk.Tk()
root.geometry("800x600")

# create a frame for the first section
frame1 = tk.Frame(root, height=200, width=400)
frame1.grid(row=0,column=0)

scrollbar_kospi = tk.Scrollbar(frame1)
scrollbar_kospi.pack(side="left",fill="y")
kospitree = ttk.Treeview(frame1)
kospitree.pack()

scrollbar_kospi.config(command=kospitree.yview)

frame2 = tk.Frame(root, height=200, width=400)
frame2.grid(row=1,column=0)

scrollbar_kosdaq = tk.Scrollbar(frame2)
scrollbar_kosdaq.pack(side="left",fill="y")
kosdaqtree = ttk.Treeview(frame2)
kosdaqtree.pack()

scrollbar_kosdaq.config(command=kosdaqtree.yview)

for i in kospistock:
    kospitree.insert('', 'end', text=f"{i}")

for i in kosdaqstock:
    kosdaqtree.insert('', 'end', text=f"{i}")

# create a frame for the second section
frame3 = tk.Frame(root, height=200, width=400)
frame3.grid(row=0,column=1)

tree = checktree.CheckboxTreeview(frame3, columns=("price",))
tree.pack(fill='both', expand=True)
# start_schedule(tree)
# Insert some items into the treeview with price values
added_items = load_txt()
for i in added_items:
    price = getPrice(i)
    tree.insert('', 'end', text=i, values=price)

def on_double_click(event, treeview):
    item = treeview.selection()[0]
    item_text = treeview.item(item, "text")
    added_items = load_txt()
    if item_text in added_items:
        return
    add_to_txt(item_text)
    added_items.append(item_text)
    print("after addition",added_items)
    
    price = getPrice(item_text)
    tree.insert('', 'end', text=item_text, values=price)

# Add columns to the treeview
tree.heading('#0', text='Item')
tree.heading('#1', text='Price')

# Set up checkboxes for each item
for item in tree.get_children():
    tree.item(item, tags=('unchecked',))
    tree.tag_bind('unchecked', '<Button-1>', lambda event: tree.item(event.tags[-1], tags=('checked',)))
    tree.tag_bind('checked', '<Button-1>', lambda event: tree.item(event.tags[-1], tags=('unchecked',)))

# Create a button to remove checked items
remove_button = tk.Button(frame3, text='Remove Checked Items', command=lambda: remove_checked_items(tree))
remove_button.pack(pady=10)

refresh_button = tk.Button(frame3, text='Refresh Market Prices',command=lambda: update_pricelist(tree))
refresh_button.pack(pady=10)

# Function to remove checked items from the treeview
def remove_checked_items(treeview):
    checked_items = treeview.get_checked()
    checked_text = []
    added_items = load_txt()
    for item in checked_items:
        item_text = treeview.item(item, 'text')
        checked_text.append(item_text)
        treeview.delete(item)
    print('Removed items:', checked_text)
    for i in checked_text:
        added_items.remove(i)
        print(added_items)
    update(added_items)

kospitree.bind("<Double-1>", lambda event: on_double_click(event, kospitree))
kosdaqtree.bind("<Double-1>", lambda event: on_double_click(event, kosdaqtree))

t1=threading.Thread(target=start_schedule,args=(tree,))
t1.start()
t1.join()
# run the main loop
root.mainloop()