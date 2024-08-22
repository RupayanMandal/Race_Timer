import time
import numpy as np
from operator import itemgetter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import random
from threading import Thread
import multiprocessing
import keyboard
import json
import sys

import customtkinter
from decimal import Decimal

#custom libraries
import tkinter_display as my_display
import my_log
import custom_database

display_on=True

def my_sort(data:dict):
    data=[{'id':i['id'],
           'lap':-i['lap'],
           'score':i['score'][0:len(i['score'])-1],
           'total_time':max(99999*int(not(bool(i['score'][-1]))) , i['score'][-1])} for i in data
           ]
    s=sorted(data,key=itemgetter('total_time','lap','score'),reverse=False)
    return list(map(itemgetter('id'),s))

def display(data: dict):
    sorted_order=my_sort(data)  
    for id in sorted_order:
        pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
        lap_text=' LAP -> {},  Rank - {}'.format(data[pos]['lap'],sorted_order.index(id)+1)
        #print(data[pos]['id'],' ',data[pos]['score'][0:6], lap_text)



def disable_event():
    pass

def quit_enable_event(app):
    #app.grab_release()
    app.protocol("WM_DELETE_WINDOW",sys.exit )

def scoreboardcalculation(lock,path,quit_val,log_lock,start_time):
    lock.acquire()
    with open(path,'r') as datafile:
        data=json.loads(datafile.read())
    lock.release()    
 
    obj = time.gmtime(0)
    paused=0
    pause_start_time=0.0
    first_car=0
    while True:
        i=keyboard.read_key()
        time.sleep(0.3)
        print("KKKKKKEEEEEEEEEEEEEYYYYYYYYYY ---> ", i,type(i))
        try:
            i=int(i)
        except:
            pass    
        if i==0 or i=='esc':
            msg="Race ENDED"
            log_lock.acquire()
            my_log.write(msg)
            my_log.savelogfile()
            log_lock.release()
            quit_val.value=1
            break
        elif i not in list(map(itemgetter('id'),data)) and i!=0:
            continue 
        else:
            if not paused:
                i=data.index(list(filter(lambda data: data['id'] == i, data))[0])
                #print(i)
                if  data[i]['lap']==len(data[i]['score']):
                    continue  
                    
                t=time.time()
                if data[i]['score'][data[i]['lap']]==0:
                    data[i]['score'][data[i]['lap']]=-t
                    if start_time.value==0:
                        start_time.value=t
                else:        
                    data[i]['score'][data[i]['lap']]=(t-abs(data[i]['score'][data[i]['lap']]))
                    msg="car {} has successfully completed lap {} in {} seconds ".format(data[i]['id'],
                                                                                         data[i]['lap']+1,
                                                                                         data[i]['score'][data[i]['lap']]           
                                                                                        )
                    log_lock.acquire()
                    my_log.write(msg)
                    log_lock.release()
                    data[i]['lap']+=1
                    start_time.value=0 
                """ 
                if data[i]['lap'] in range (1,len(data[i]['score'])+1):
                    data[i]['score'][data[i]['lap']-1]=(t-abs(data[i]['score'][data[i]['lap']-1]))-pause_timer.value
                    
                    log_lock.acquire()
                    my_log.write(msg)
                    log_lock.release()
                    
                    if data[i]['lap']==len(data[i]['score'])-1:
                        data[i]['score'][len(data[i]['score'])-1]=data[i]['score'][len(data[i]['score'])-2]
                        msg="car {} has successfully completed THE RACE in {} seconds ".format(data[i]['id'],
                                                                                         data[i]['score'][len(data[i]['score'])-1]           
                                                                                         )
                        log_lock.acquire()
                        my_log.write(msg)
                        log_lock.release()    
                 """        
                
                   
                lock.acquire()
                with open(path,'w+') as datafile:
                    json.dump(data,datafile)
                lock.release() 
                display(data)
                #tk_display(table,data)

            

def scoreboarddisplay(lock,path,quit_val,log_lock,start_time,number_of_participants,number_of_laps):    

    def tk_display(tk_main_window,detail_table,rank_table,path,log_text_widget,log_lock,elapsed_time,current_leader):
        lock.acquire()
        with open(path,'r') as datafile:
            data=json.loads(datafile.read())
        lock.release()
        #print(data)
        #print('#######################################################')
        sorted_order=my_sort(data) 
        temp_elapsed_time=0.00
        if start_time.value!=0.00:
            temp_elapsed_time=round(Decimal(time.time()-start_time.value),3)
        if start_time.value==-1:
            temp_elapsed_time=0
        if quit_val.value==0 :
            elapsed_time.configure(text='ELAPSED TIME\n{}'.format(temp_elapsed_time))
        temp=1
        for id in sorted_order:
            pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
            if temp==1:
                current_leader.configure(text='CURRENT LEADER\n{}'.format(data[pos]['name']))
            min_elm = 99999
            for lap_number in range(len(data[pos]['score'])): 
                i=data[pos]['score'][lap_number]   
                if i > 0 and i< min_elm:
                    min_elm = i
            if min_elm == 99999:
                  best_lap="N/A"
            else:
                best_lap= round(Decimal(min_elm),3)
            display_arr=[sorted_order.index(id)+1, 
                         data[pos]['name'],
                         data[pos]['lap'],
                         best_lap]
            #print(display_arr)
            rank_table.update_rows(temp,display_arr)
            temp+=1
        temp=1
        temp_id=sorted_order
        temp_id.sort()

        for id in temp_id:
            pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
            display_arr=[data[pos]['id'],data[pos]['name']]
            display_arr.extend([round(Decimal(max(i,0)),3) for i in data[pos]['score']])
            #print(display_arr)
            detail_table.update_rows(temp,display_arr)
            temp+=1
        
        if quit_val.value==0:
            tk_main_window.protocol("WM_DELETE_WINDOW", disable_event)
        else:
            tk_main_window.protocol("WM_DELETE_WINDOW", quit_enable_event(tk_main_window))
        
        log_display(log_text_widget,log_lock)
        tk_main_window.after(3, tk_display,tk_main_window, detail_table,rank_table,path,log_text_widget,log_lock,elapsed_time,current_leader)

    def log_display(text_widget,log_lock):
        
        log_lock.acquire()
        msg=my_log.read()
        log_lock.release()
        #text_widget.config(state='normal')
        text_widget.delete(1.0,END)
        text_widget.insert(END,msg) 
        text_widget.yview(END)
        #text_widget.config(state='disabled')   


    root=customtkinter.CTk()
    root.title('TIME TRIAL')
    root.attributes('-topmost',True)
    #root.grab_set()
    root_widgets=[]
    #root widgets
    display_label_name=customtkinter.CTkLabel(master=root,padx=10,fg_color='Black',font=('Courier',18,'bold'),text='SCORE BOARD',justify='left')
    root_widgets.append(display_label_name)
    
    display_label=customtkinter.CTkFrame(master=root,fg_color='Black')
    root_widgets.append(display_label)
    
    info_label_name=customtkinter.CTkLabel(master=root,padx=10,fg_color='Black',font=('Courier',18,'bold'),text='LOG',justify='left')
    root_widgets.append(info_label_name)

    info_label=customtkinter.CTkFrame(master=root,fg_color="Black")
    root_widgets.append(info_label)
    
    
    
    
    #widgets
        #1. score display table
    my_col_names_rank=['  RANK  ','  NAME  ',' CURRENT LAP ',' BEST LAP TIME ']
    my_col_names_detail=['  ID  ',' NAME ']
    my_col_names_detail.extend(['  LAP {}  '.format(i+1) for i in range(number_of_laps)])
    
    
    my_table_rank = my_display.Table(root=display_label,
                                     rows=number_of_participants+1,
                                     cols=len(my_col_names_rank),
                                     col_names=my_col_names_rank)
    
    elapsed_time= customtkinter.CTkLabel(master=display_label,fg_color="transparent",text_color='green',justify='center')
    current_leader= customtkinter.CTkLabel(master=display_label,fg_color="transparent",text_color='orange',justify='center')

    my_table_detail = my_display.Table(root=display_label,
                                       rows=number_of_participants+1,
                                       cols=len(my_col_names_detail),
                                       col_names=my_col_names_detail)
        #2 info display table 
    race_current_stat=customtkinter.CTkTextbox(info_label,fg_color='transparent',text_color='red',
                        font=('Courier',10), wrap='word',
                        xscrollcommand=False,yscrollcommand=False,
                        )
    #packing
    for my_frame_number in range(len(root_widgets)):
        root_widgets[my_frame_number].grid(row=my_frame_number,column=0,sticky="nsew")

    ## inside display label
    my_table_rank.table.grid(row=0,column=0,rowspan=2,sticky='nsew',padx=10,pady=10)
    elapsed_time.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)
    current_leader.grid(row=1,column=1,sticky='nsew',padx=10,pady=10)  
    my_table_detail.table.grid(row=2,column=0,columnspan=2,sticky='nsew',padx=10,pady=10)
        
    ## inside info label
    race_current_stat.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
    
    #row and column configure
    root.rowconfigure(list(range(len(root_widgets))),weight=1)
    root.columnconfigure(0,weight=1)
    
    for i in root_widgets:
        if isinstance(i,customtkinter.CTkFrame):
            col,row=i.grid_size()
            if col!=0:
                col=list(range(col))
            if row!=0:
                row=list(range(row))    
            i.rowconfigure(row,weight=1)
            i.columnconfigure(col,weight=1)
            
    
    #table.update(1,4,'Hello')
    tk_display(root,my_table_detail,my_table_rank,path,race_current_stat,log_lock,elapsed_time,current_leader)
    #log_display(race_current_stat,log_lock)
        
    #root.after(1, tk_display, table, data)
    root.mainloop()    




class time_trial_race():
    def __init__(self,number_of_laps,participant_name_list: list):
        data = []
        db=custom_database.database('my_sql.db')

        for i in participant_name_list:
            d={'id':i ,'name':db.run('SELECT NAME FROM TEAMS WHERE ID={};'.format(i))[0][0] ,'lap':0, 'score': [0.0]*(number_of_laps)}
            data.append(d)

        my_log.clearlogfile()
        my_log.write("Race STARTED")
        path='score.txt'

        with open(path,'w+') as datafile:
            json.dump(data,datafile)
    
    
        lock=multiprocessing.Lock()
        log_lock=multiprocessing.Lock()
        quit_val = multiprocessing.Value('i', 0)
        #pause_timer=multiprocessing.Value('d',0.0)
        start_time=multiprocessing.Value('d',0.0)
                        
        processes = []

        p1 = multiprocessing.Process(target=scoreboardcalculation,args=(lock,path,quit_val,log_lock,start_time))
        p2 = multiprocessing.Process(target=scoreboarddisplay,args=(lock,path,quit_val,log_lock,start_time,len(data),number_of_laps))
        processes.append(p1)
        processes.append(p2)

        p1.start()
        p2.start()
        # Waiting for all processes to complete
        for p in processes:
            p.join()
        print("All tasks completed")

if __name__=='__main__':
    time_trial_race(2,[1,2])        