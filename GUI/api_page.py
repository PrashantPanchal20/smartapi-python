#=========================================================== TAB 4 company stock data ================================
import sys
sys.path.append('D:/Prashant/smartapi-python') 
from example.get_token import *
from tkinter import *
import tkinter as ttk
import tkinter as tk
import pandas as pd
from tkinter import ttk

#  [[173.5, 173.5, 165.25, 167.14999389648438, 167.14999389648438, 74224.0], [166.75, 169.75, 164.35000610351562, 166.89999389648438, 166.89999389648438, 63791.0], [169.0, 177.6999969482422, 166.0500030517578, 175.60000610351562, 175.60000610351562, 242415.0]]
# ['Open' 'High' 'Low' 'Close' 'Adj Close' 'Volume']

def on_select(event):
    # Get selected item(s)
    selected_item = tree.selection()
    
    # Iterate over selected items
    for item in selected_item:
        # Retrieve values of the selected item
        values = tree.item(item, "values")
        print("Selected values:", values)

treeview_exists = False
def create_widgets(dataframe):
    global treeview_exists, tree
    # print(dataframe.head(10))
    data =dataframe.values.tolist()
    df_col = dataframe.columns.values
    df_col = df_col.tolist()
# Split each string in the list based on spaces
    # for i in range(len(df_col)):
    #     df_col[i] = df_col[i].split()
    # single_list = [item for sublist in df_col for item in sublist]
    # split_data = [item.split() for sublist in data for item in sublist]
    if not treeview_exists:
        tree = ttk.Treeview(tab4_frame2, columns = ('0','1','2', '3', '4'), show= 'headings')
        tree.pack(fill= 'both', expand= True)
        tree.bind("<<TreeviewSelect>>", on_select)
        treeview_exists = True

        for col in range(len(df_col)):
            tree.column(col, width=100, anchor=tk.CENTER)
            tree.heading(col, text=df_col[col])

        for row in tree.get_children():
                tree.delete(row)

        for row in data:
            tree.insert('', 'end', values=row)


def display_data():
    global df
    df = pd.read_csv('company_token_list.csv', index_col=False, low_memory=False)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', None)
    # df.rename(columns={df.columns[0]: 'Index'}, inplace=True)
    # df.rename(columns={df.columns[0]: 'Index token symbol name instrumenttype exch_seg'}, inplace=True)
    create_widgets(df)

def create_labeled_frame(root, label_text, frame_height):
    frame = LabelFrame(root, text=label_text, height=frame_height)
    frame.pack(fill = 'x')
    return frame

def api_tab_design(tab4):
    global data_text, tab4_frame2

    tab4_frame0 = Frame(tab4, background="pink", height = 120)
    tab4_frame0.pack(fill="x")

    frame1 = create_labeled_frame(tab4_frame0, "Welcome ::", 60)
    # label1 = ttk.Label(frame1, text="")
    # label1.pack()
    button_getOI_chart = ttk.Button(frame1, text= 'Update token List! '' Click Once in a day. It will take time',width = 45, command = get_token_api)
    button_getOI_chart.place(x=10, y=5)

    button_getOI_chart = ttk.Button(frame1, text= 'Get token List!',width = 15, command = display_data)
    button_getOI_chart.place(x=410, y=5)

    tab4_frame1 = Frame(tab4, background="yellow",width=150)
    tab4_frame1.pack(side= 'left', fill = 'y')

    tab4_frame2 = Frame(tab4,background="blue", height=450)
    tab4_frame2.pack(fill= 'x')

    tab4_frame3 = Frame(tab4,background="pink", height=150)
    tab4_frame3.pack(fill= 'x')
