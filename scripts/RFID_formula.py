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

import customtkinter
from decimal import Decimal
import serial

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


def scoreboardcalculation(lock,path,quit_val,pause_timer,log_lock,start_time,number_of_laps,com_port):
    listener=serial.Serial(port="COM{}".format(com_port),baudrate=9600,timeout=1)
            
    lock.acquire()
    with open(path,'r') as datafile:
        data=json.loads(datafile.read())
    lock.release()    
    print(data)
    obj = time.gmtime(0)
    paused=0
    pause_start_time=0.0
    first_car=0
    while True:
        #i=keyboard.read_key()
        i=1
        id=str(listener.readline())
        #print(temp)
        if id=="b''":
            continue
        id=''.join([i for i in id if i.isdigit()])
        if id!='' and id!=' ':
            id=int(id)
            print(id)
    
        #print("KKKKKKEEEEEEEEEEEEEYYYYYYYYYY ---> ", i,type(i))
        try:
            i=int(i)
        except:
            pass    
        if sum(list(map(itemgetter('lap'), data)))==len(data)*(number_of_laps+1):
            msg="Race ENDED"
            log_lock.acquire()
            my_log.write(msg)
            my_log.savelogfile()
            log_lock.release()
            quit_val.value=1
            break
        elif i=='p':
            paused=1-paused
            print(paused)
            if paused==1:
                msg="Race PAUSED"
                log_lock.acquire()
                my_log.write(msg)
                log_lock.release()
                
                if pause_start_time==0.0:
                    pause_start_time=time.time()
            else :
                temp=max(0.0,time.time()-pause_start_time)
                pause_timer_value=pause_timer.value
                pause_timer_value+=temp
                pause_timer.value=pause_timer_value
                pause_start_time=0.0
                start_time=0.0
                msg="Race RESUMED after a pause of {} seconds \n \t\t\t\tTotal pause time = {} seconds".format(temp,pause_timer_value)
                log_lock.acquire()
                my_log.write(msg)
                log_lock.release()
                print('+++++++++++++++++++++++++++++++++ ',pause_timer)
                        

        elif id not in list(map(itemgetter('id'),data)) and id!=0:
            continue 
        else:
            print(id)
            if not paused:
                i=data.index(list(filter(lambda data: data['id'] == id, data))[0])
                #print(i)
                if  data[i]['score'][len(data[i]['score'])-1]!=0:
                    continue  
                    
                t=time.time()
                if data[i]['score'][data[i]['lap']]==0:
                    if not first_car:
                        first_car=-t
                        if not start_time.value:
                            start_time.value=time.time()
    
                    data[i]['score'][data[i]['lap']]=first_car         
                else:
                    data[i]['score'][data[i]['lap']]=-t
                
                if data[i]['lap'] in range (1,len(data[i]['score'])+1):
                    data[i]['score'][data[i]['lap']-1]=(t-abs(data[i]['score'][data[i]['lap']-1]))-pause_timer.value
                    msg="car {} has successfully completed lap {} in {} seconds ".format(data[i]['id'],
                                                                                         data[i]['lap'],
                                                                                         data[i]['score'][data[i]['lap']-1]           
                                                                                         )
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
                data[i]['lap']+=1
                   
                lock.acquire()
                with open(path,'w+') as datafile:
                    json.dump(data,datafile)
                lock.release() 
                display(data)
                #tk_display(table,data)

            

def scoreboarddisplay(lock,path,quit_val,log_lock,start_time,pause_timer,number_of_participants,number_of_laps):    

    def tk_display(tk_main_window,detail_table,rank_table,path,log_text_widget,log_lock,elapsed_time,current_leader,pause_timer):
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
        if quit_val.value==0:
            elapsed_time.configure(text='ELAPSED TIME\n{}\n(-{})'.format(temp_elapsed_time,round(Decimal(pause_timer.value),3)))
        temp=1
        for id in sorted_order:
            pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
            
            if temp==1:
                current_leader.configure(text='CURRENT LEADER\n{}'.format(data[pos]['name']))
            
            min_elm = 99999
            for lap_number in range(len(data[pos]['score'])-1): 
                if lap_number==0:
                    i=data[pos]['score'][lap_number]
                else:
                    i=data[pos]['score'][lap_number]-data[pos]['score'][lap_number-1]    
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
            display_arr.extend([round(Decimal(max(i,0)),3) for i in data[pos]['score'][:len(data[pos]['score'])-1]])
            #print(display_arr)
            detail_table.update_rows(temp,display_arr)
            temp+=1
        
        if quit_val.value==0:
            tk_main_window.protocol("WM_DELETE_WINDOW", disable_event)
        else:
            tk_main_window.protocol("WM_DELETE_WINDOW", quit)
        
        log_display(log_text_widget,log_lock)
        tk_main_window.after(3, tk_display,tk_main_window, detail_table,rank_table,path,log_text_widget,log_lock,elapsed_time,current_leader,pause_timer)

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
    root.title('FORMULA RACE')
    root.attributes('-topmost',True)
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
    my_col_names_detail=['  ID  ', ' NAME ']
    my_col_names_detail.extend(['  LAP {}  '.format(i+1) for i in range(number_of_laps)])
    #my_col_names_detail.extend([' FINAL Time'])
    
    
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
    tk_display(root,my_table_detail,my_table_rank,path,race_current_stat,log_lock,elapsed_time,current_leader,pause_timer)
    #log_display(race_current_stat,log_lock)
        
    #root.after(1, tk_display, table, data)
    root.mainloop()    




class formula_race():
    def __init__(self,com_port,number_of_laps,participant_name_list: list):
        data = []
        db=custom_database.database('my_sql.db')
        for i in participant_name_list:
            d={'id':i ,'name': db.run('SELECT NAME FROM TEAMS WHERE ID={}'.format(i))[0][0],'lap':0, 'score': [0.0]*(number_of_laps+1)}
            data.append(d)

        my_log.clearlogfile()
        my_log.write("Race STARTED")
        path='score.txt'

        with open(path,'w+') as datafile:
            json.dump(data,datafile)
    
    
        lock=multiprocessing.Lock()
        log_lock=multiprocessing.Lock()
        quit_val = multiprocessing.Value('i', 0)
        pause_timer=multiprocessing.Value('d',0.0)
        start_time=multiprocessing.Value('d',0.0)
                        
        processes = []

        p1 = multiprocessing.Process(target=scoreboardcalculation,args=(lock,path,quit_val,pause_timer,log_lock,start_time,number_of_laps,com_port))
        p2 = multiprocessing.Process(target=scoreboarddisplay,args=(lock,path,quit_val,log_lock,start_time,pause_timer,len(data),number_of_laps))
        processes.append(p1)
        processes.append(p2)

        p1.start()
        p2.start()
        # Waiting for all processes to complete
        for p in processes:
            p.join()
        print("All tasks completed")

if __name__=='__main__':
    formula_race(6,2,[83150223167,969414427])        