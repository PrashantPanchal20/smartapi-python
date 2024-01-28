import sys
# sys.path.append('/home/ppanchal/Prashant_Panchal/GUI/site-packages/')
import tkinter
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedTk
import time
import option_chain as op_chain
from datetime import datetime
import threading
import Equity_Data as eq_data
# import chart_all as chart
import autocompletecombobox as autocomp
import sys, os, atexit
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from api_page import api_tab_design


def update_clk():
    now = datetime.now()
    time_txtbox.insert("1.0",f'"Time and Date" :: {now.strftime("%H:%M:%S, %Y-%m-%d")}')
    time_txtbox.after(1000, update_clk)

def get_op_chain():

    index_name = index_combobox.get()
    num_strike = numstrike_combobox.get()

    def update_op_data():
        op_chain.data_fetch(index_name, num_strike)  # function call with index name 
        df = op_chain.data_frame_OP
        data =df.values.tolist()
        df_col = df.columns.values

        underlying_box.config(state= 'normal')
        res_lable_box.config(state= 'normal')
        sup_lable_box.config(state= 'normal')
        change_oi_box_call.config(state= 'normal')
        change_oi_box_put.config(state= 'normal')
        max_vol_call_box.config(state= 'normal')
        max_vol_put_box.config(state= 'normal')
        PCR_Lable_box.config(state= 'normal')

        underlying_box.delete('1.0',END)
        res_lable_box.delete('1.0',END)
        sup_lable_box.delete('1.0',END)
        change_oi_box_call.delete('1.0',END)
        change_oi_box_put.delete('1.0',END)
        max_vol_call_box.delete('1.0',END)
        max_vol_put_box.delete('1.0',END)
        PCR_Lable_box.delete('1.0',END)

        underlying_box.insert('1.0', op_chain.header_values)
        res_lable_box.insert('1.0', f'"On Strike" :: {op_chain.max_oi_strike_CE} , "OI" = {op_chain.max_oi_CE}')
        sup_lable_box.insert('1.0', f'"On Strike" :: {op_chain.max_oi_strike_PE} , "OI" = {op_chain.max_oi_PE}')
        max_vol_call_box.insert('1.0', f'"On Strike" :: {op_chain.max_vol_strike_CE} , "Volume" = {op_chain.max_vol_CE}')
        max_vol_put_box.insert('1.0', f'"On Strike" :: {op_chain.max_vol_strike_PE} , "Volume" = {op_chain.max_vol_PE}')
        change_oi_box_call.insert('1.0', f'"On Strike" :: {op_chain.Change_OI_strike_CE} , "Today Change OI" = {op_chain.Change_OI_CE}')
        change_oi_box_put.insert('1.0', f'"On Strike" :: {op_chain.Change_OI_strike_PE} , "Today Change OI" = {op_chain.Change_OI_PE}')
        PCR_Lable_box.insert('1.0', f'"OverAll PCR" :: {op_chain.total_pcr} , " Today PCR basis on Change OI" = {op_chain.currentday_pcr}')

        underlying_box.config(state= 'disabled')
        res_lable_box.config(state= 'disabled')
        sup_lable_box.config(state= 'disabled')
        change_oi_box_call.config(state= 'disabled')
        change_oi_box_put.config(state= 'disabled')
        max_vol_call_box.config(state= 'disabled')
        max_vol_put_box.config(state= 'disabled')
        PCR_Lable_box.config(state= 'disabled')

        for x in range(len(df_col)):
            table.column(x, width=100 )
            table.heading(x, text=df_col[x])

        for row in table.get_children():
            table.delete(row)

        for y in reversed(range(len(data))):
            table.insert('', 0, values=(df.iloc[y,:].to_list()))
        
        threading.Timer(5.0, update_op_data).start()
        plot_OI(op_chain.data_frame_OP)

    update_op_data()

def plot_OI(data_frame_OP):
    global strike, call_oi
    
    strike = []
    call_oi = []

    for item in data_frame_OP['Call OI']:
        call_oi.append(int(item.strip()))

    for item in data_frame_OP['STRIKE']:
        strike.append(item)


def _main_window():
    global index_combobox, Label_frame, table, underlying_box, numstrike_combobox, res_lable_box, sup_lable_box, time_txtbox
    global change_oi_box_call, change_oi_box_put, max_vol_call_box, max_vol_put_box, PCR_Lable_box

    window = ThemedTk(theme='arc', )
    window.title("Think More and more, Be Continue")
    window.geometry("1300x800")
    style = ttk.Style(window)
    style.configure('.', font=('Times New Roman',10))
    style.configure('TButton', font=('Helvetica', 11))
    tabControl = ttk.Notebook(window)

    global tab1, tab2, tab3, tab4, chain_txtbox, chain_txtbox1
    tab1 = ttk.Frame(tabControl,padding=5)
    tab2 = ttk.Frame(tabControl,padding=5)
    tab3 = ttk.Frame(tabControl,padding=5)
    tab4 = ttk.Frame(tabControl,padding=5)

    tabControl.add(tab1, text="   Option Chain ")
    tabControl.add(tab2, text="  Graph Dashboard  ")
    tabControl.add(tab3, text=" Company Stock Data ")
    tabControl.add(tab4, text=" Angel One API ")
    tabControl.pack(fill = BOTH, expand = True)
#===============================================================  TAB 1 : UI =============================================== 
    tab1_frame0 = Frame(tab1, height=100) #background="yellow"
    tab1_frame0.pack(side="top", fill="x")

    txt0 = Label(tab1_frame0, text="Choose Index here :: ")
    txt0.place(x=20, y=20)
    index_combobox = ttk.Combobox(tab1_frame0, values= ("NIFTY", "BANKNIFTY","FINNIFTY", "MIDCPNIFTY"))
    index_combobox.place(x=180, y=20)
    index_combobox['state'] = 'readonly'

    txt0 = Label(tab1_frame0, text="No of Strikes :: ")
    txt0.place(x=400, y=20)
    numstrike_combobox = ttk.Combobox(tab1_frame0, values= ("5", "10", "15", "20"))
    numstrike_combobox.place(x=500, y=20)
    numstrike_combobox.set('10')
    numstrike_combobox['state'] = 'readonly'
    
    def tab_change():
        tabControl.select(tab4)
        # plot_OI(op_chain.data_frame_OP)


    button0 = Button(tab1_frame0, text= "Continue ",command = get_op_chain)
    button0.place(x=720, y=20)
    button_graph = Button(tab1_frame0, text= "Angel One API : Click Here ! ", command= tab_change)
    button_graph.place(x=1000, y=20)

    underlying_txt = Label(tab1_frame0, text= "UnderLying Index :: ")
    underlying_txt.place(x=21, y=60)
    underlying_box = Text(tab1_frame0, width= 60, height=1, bg = 'cyan', foreground= 'black', font=("Arial 14", 14, "bold"),state= 'disabled')
    underlying_box.place(x=180, y=60)

    time_txtbox = Text(tab1_frame0, width=40, height=1, foreground='red', font=("Arial 12", 12, "bold"))
    time_txtbox.place(x=900, y=60)

    tab1_frame1 = Frame(tab1)
    tab1_frame1.pack(fill= "both", expand= True)

    Label_frame = LabelFrame(tab1_frame1, text=" Option Chain ")
    Label_frame.pack(fill= "both", expand= True)
    yscrollbar = ttk.Scrollbar(Label_frame, orient= 'vertical')
    yscrollbar.pack(side = "right", fill='y')
    xscrollbar = ttk.Scrollbar(Label_frame, orient= 'horizontal')
    xscrollbar.pack(side = "bottom", fill = "x")
    table = ttk.Treeview(Label_frame, columns=('0','1','2', '3', '4', '5','6','7','8','9','10','11','12','13'), show= 'headings')
    table.pack(fill= 'both', expand= True, anchor= 'center')
    # table.insert('', 'end', values=("WELCOME \nOption Chain Will show here. Please select index and Continuo :: >>","#00ff00"))
    # table.column(0, width=100,stretch=TRUE)
    table.xview_scroll(1, 'units')
    xscrollbar.config(command = table.xview)
    yscrollbar.config(command = table.yview)

    tab1_frame2 = Frame(tab1)
    tab1_frame2.pack(fill= "both", expand= True)

    res_lable = Label(tab1_frame2, text= 'Major Resistance ::')
    res_lable.place(x=20, y=20)
    res_lable_box = Text(tab1_frame2, width=45, height=1,  bg = 'lightblue', foreground= 'black', font=("Arial 14", 14, "bold"),state='disabled')
    res_lable_box.place(x=150, y=20)

    sup_lable = Label(tab1_frame2, text= 'Major Support ::')
    sup_lable.place(x=700, y=20)
    sup_lable_box = Text(tab1_frame2, width=50, height=1,  bg = 'pink', foreground= 'black', font=("Arial 14", 14, "bold"), state='disabled')
    sup_lable_box.place(x=800, y=20)

    change_oi_lable_call = Label(tab1_frame2, text= 'Max Change OI ::')
    change_oi_lable_call.place(x=20, y=60)
    change_oi_box_call = Text(tab1_frame2, width=45, height=1,  bg = 'lightblue', foreground= 'black', font=("Arial 14", 14, "bold"),state='disabled')
    change_oi_box_call.place(x=150, y=60)

    change_oi_lable_put = Label(tab1_frame2, text= 'Max Change OI ::')
    change_oi_lable_put.place(x=700, y=60)
    change_oi_box_put = Text(tab1_frame2, width=50, height=1,  bg = 'pink', foreground= 'black', font=("Arial 14", 14, "bold"), state='disabled')
    change_oi_box_put.place(x=800, y=60)

    max_vol_call = Label(tab1_frame2, text= 'Max Call Volume ::')
    max_vol_call.place(x=20, y=100)
    max_vol_call_box = Text(tab1_frame2, width=45, height=1,  bg = 'lightblue', foreground= 'black', font=("Arial 14", 14, "bold"),state='disabled')
    max_vol_call_box.place(x=150, y=100)

    max_vol_put = Label(tab1_frame2, text= 'Max Put Volume ::')
    max_vol_put.place(x=690, y=100)
    max_vol_put_box = Text(tab1_frame2, width=50, height=1,  bg = 'pink', foreground= 'black', font=("Arial 14", 14, "bold"), state='disabled')
    max_vol_put_box.place(x=800, y=100)

    PCR_Lable = Label(tab1_frame2, text= 'Put Call Ratio ::')
    PCR_Lable.place(x=20, y=150)
    PCR_Lable_box = Text(tab1_frame2, width=70, height=1,  bg = 'lightblue', foreground= 'black', font=("Arial 14", 14, "bold"),state='disabled')
    PCR_Lable_box.place(x=150, y=150)

    # sup_lable = Label(tab1_frame2, text= 'Major Support ::')
    # sup_lable.place(x=650, y=20)
    # sup_lable_box = Text(tab1_frame2, width=50, height=1,  bg = 'pink', foreground= 'black', font=("Arial 14", 14, "bold"), state='disabled')
    # sup_lable_box.place(x=800, y=20)

#=========================================================== TAB 2 Graphs =====================

    # def clear():
    #     for item in Canvas1.get_tk_widget().find_all():
    #         Canvas1.get_tk_widget().delete(item)

    def get_oi_char():
        global Canvas1, fig1
        def update():
            for widget in tab2_frame1.winfo_children():
                widget.destroy()

            fig1, df = plt.subplots()
            width = 20 
            df.bar(strike, call_oi, width= width)
            # plt.xticks(np.arange(min(strike), max(strike), 1.0))
            print(call_oi)
            print(strike)

            for i,v in enumerate(call_oi):
                plt.text(i,v+6000 ,str(v), ha = CENTER, size = 100, color = "red")

            # plt.tight_layout()
            plt.xlabel("STRIKES -->")
            plt.ylabel("Call OI Canvas1 -->")

            Canvas1 = FigureCanvasTkAgg(fig1, tab2_frame1)
            Canvas1.draw()
            Canvas1.get_tk_widget().pack(fill= 'both')
            

    tab2_frame0 = Frame(tab2,background="yellow",width=200)
    tab2_frame0.pack(side= 'left', fill="y")

    button_getOI_chart = Button(tab2_frame0, text= 'Get OI Data on Graph. ', command= get_oi_char)
    button_getOI_chart.place(x=20, y=50)

    tab2_frame1 = Frame(tab2,background="blue", height=650)
    tab2_frame1.pack(fill= 'x')



#=========================================================== TAB 3 company stock data =====================
    # tab3_frame0 = Frame(tab3, height=60, background="yellow")
    # tab3_frame0.pack(side="top", fill="x")

    # lable_all_comp = Label(tab3_frame0, text= "For seeing The all Equites Company Inforamtion. :: ")
    # lable_all_comp.place(x= 20, y=20)

    def comp_data():
        eq_data.quity_data()
        df1 = eq_data.equity_details
        data1 =df1.values.tolist()
        df_col1 = df1.columns.values
        # print(df1)

        for x in range(len(df_col1)):
            table1.column(x, width=100 )
            table1.heading(x, text=df_col1[x])

        for row in table.get_children():
            table1.delete(row)

        for y in reversed(range(len(data1))):
            table1.insert('', 0, values=(df1.iloc[y,:].to_list()))
        

    tab3_frame0 = Frame(tab3,background='blue')
    tab3_frame0.pack(fill="x")

    lable_frame = LabelFrame(tab3_frame0,text= "All Equity Companies Inforamtion Here :: ")
    lable_frame.pack(fill='x')
    # txt_box = Text(lable_frame)
    # txt_box.pack(fill= "both")
    table1 = ttk.Treeview(lable_frame, columns=('0','1','2', '3', '4', '5','6','7'), show= 'headings',height=17)
    table1.pack(fill= 'both', expand= True)
    table1.column("0", width=40,stretch=True) 
    table1.column("1",minwidth=0,width = 200, stretch=True) 
    try:
        comp_data()
    except:
        pass

    tab3_frame1 = Frame(tab3, height=40)
    tab3_frame1.pack(fill= 'x')

    def check_call(event):
        symbol = event.widget.get()
        eq_data.check_data(symbol)
        # print(eq_data.data)
        # print(type(eq_data.data))
        df2 = eq_data.data
        data2 =df2.values.tolist()
        df_col2 = df2.columns.values
        # print(df1)
        print(data2)
        print(df_col2)

        for x in range(len(df_col2)):
            table2.column(x, width=100 )
            table2.heading(x, text=df_col2[x])

        for row in table2.get_children():
            table2.delete(row)

        for y in reversed(range(len(data2))):
            table2.insert('', 0, values=(df2.iloc[y,:].to_list()))
        
    def down_data():
        symbol = symbol_combobox.get()
        eq_data.export_data(symbol)

    comp_button = Button(tab3_frame1, text="Refresh Data", command=comp_data)
    comp_button.place(x=20, y=5)
    
    symbol_combobox = autocomp.AutocompleteCombobox(tab3_frame1,completevalues= eq_data.symbol)
    symbol_combobox.place(x=200, y=5)
    symbol_combobox.bind("<<ComboboxSelected>>", check_call)
  
    check_file = Button(tab3_frame1, text='Download Data', command = down_data )
    check_file.place(x=400, y=5)

    tab3_frame2 = Frame(tab3, background='red')
    tab3_frame2.pack(fill= 'both')

    table2 = ttk.Treeview(tab3_frame2, columns=('0','1','2', '3', '4', '5'), show= 'headings',height=17)
    table2.pack(fill= 'both', expand= True)

    op_field = tkinter.Text(tab3_frame2)
    op_field.pack(fill = BOTH, expand = True)
    op_field.xview_scroll(1, 'units')

    api_tab_design(tab4)
    update_clk()
    window.mainloop()

import sys
sys.path.append('D:\Prashant\smartapi-python') 
from example.get_token import get_token_api

if __name__ == "__main__" :
        # get_token_api()
        _main_window()
        
        
