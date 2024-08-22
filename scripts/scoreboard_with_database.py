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
import CTkTable
from decimal import Decimal

#custom libraries
import tkinter_display as my_display
import my_log
import custom_database

display_on=True

def my_sort(lock,db,number_of_laps):
    """ data=[{'id':i['id'],
           'lap':-i['lap'],
           'score':i['score'][0:len(i['score'])-1],
           'total_time':max(99999*int(not(bool(i['score'][-1]))) , i['score'][-1])} for i in data
           ]
    s=sorted(data,key=itemgetter('total_time','lap','score'),reverse=False)
    return list(map(itemgetter('id'),s)) """
    laps_list=['LAP{}'.format(i) for i in range(number_of_laps,0,-1)]
    ordering_laps=' ASC,'.join(laps_list)
    laps=','.join("FORMAT('%2.3f',{})".format(i) for i in laps_list[::-1])

    query="SELECT ID FROM RACE ORDER BY CURRENT_LAP DESC ,{};".format(ordering_laps)
    lock.acquire()
    rank_list=db.run(query)
    for i in range(len(rank_list)):
        db.run("UPDATE RACE SET RANK={} WHERE ID={};".format(i+1,rank_list[i][0]))
    
    query_detailed="SELECT NAME,{} FROM RACE ORDER BY RANK;".format(laps)
    
    coalesce_nullif_lap_query=','.join(['COALESCE(NULLIF(LAP{},0.0),99999)'.format(i) for i in range(1,number_of_laps+1)])
    min_time_query='MIN({})'.format(coalesce_nullif_lap_query)
    best_time_query="COALESCE(NULLIF({},99999),'NA')".format(min_time_query)
    query_ranked="SELECT RANK,NAME,CURRENT_LAP,FORMAT('%2.3f',{}) FROM RACE ORDER BY RANK;".format(best_time_query)
    
    result_detailed=db.run(query_detailed)
    result_ranked=db.run(query_ranked)
    lock.release()
    
    return result_detailed,result_ranked

""" def display(data: dict):
    sorted_order=my_sort(data)  
    for id in sorted_order:
        pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
        lap_text=' LAP -> {},  Rank - {}'.format(data[pos]['lap'],sorted_order.index(id)+1)
        #print(data[pos]['id'],' ',data[pos]['score'][0:6], lap_text)
 """


def disable_event():
    pass


def scoreboardcalculation(lock,quit_val,pause_timer,log_lock,start_time):
    db=custom_database.database("my_sql.db")    
    """ lock.acquire()
    with open(path,'r') as datafile:
        data=json.loads(datafile.read())
    lock.release()    
  """
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
            #my_log.savelogfile()
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
                        

        else:
            if not paused:
                lock.acquire()
                total_lap=db.run("SELECT TOTAL_LAP FROM RACE;")[0][0]
                current_lap=db.run("SELECT CURRENT_LAP FROM RACE WHERE ID={};".format(i))[0][0]
                lock.release()
                #print(i)
                if  current_lap>total_lap:
                    continue  
                    
                t=time.time()
                #if data[i]['score'][data[i]['lap']]==0:
                
                lock.acquire()
                current_lap=db.run("SELECT CURRENT_LAP FROM RACE WHERE ID={};".format(i))[0][0]
                
                if current_lap<total_lap: 
                    if db.run("SELECT LAP{} FROM RACE WHERE ID={};".format(current_lap+1,i))[0][0]==0.0 :
                        if not first_car:
                            first_car=t
                            if not start_time.value:
                                start_time.value=time.time()
    
                    #data[i]['score'][data[i]['lap']]=first_car
                        temp_time=first_car
                             
                    else:
                        temp_time=t

                    db.run("UPDATE RACE SET LAP{}={} WHERE ID={};".format(current_lap+1,temp_time,i))
                
                if current_lap in range (1,total_lap+1):
                    #data[i]['score'][data[i]['lap']-1]=(t-abs(data[i]['score'][data[i]['lap']-1]))-pause_timer.value
                    
                    temp_main_time=t-pause_timer.value
                    db.run("UPDATE RACE SET LAP{}={}-ABS(LAP{}) WHERE ID={};".format(current_lap,
                                                                                    temp_main_time,
                                                                                    current_lap,
                                                                                    i
                                                                                    ))
                    msg="TEAM {} has successfully completed lap {} in {} seconds ".format(db.run("SELECT NAME FROM RACE WHERE ID={};".format(i))[0][0],
                                                                                         current_lap,
                                                                                         db.run("SELECT LAP{} FROM RACE WHERE ID={};".format(current_lap,i))[0][0]           
                                                                                         )
                    log_lock.acquire()
                    my_log.write(msg)
                    log_lock.release()
                    
                    if current_lap==total_lap:
                        msg="TEAM {} has successfully the race in {} seconds ".format(db.run("SELECT NAME FROM RACE WHERE ID={};".format(i))[0][0],
                                                                                         db.run("SELECT LAP{} FROM RACE WHERE ID={};".format(current_lap,i))[0][0]           
                                                                                         )
                        log_lock.acquire()
                        my_log.write(msg)
                        log_lock.release()    
                
                db.run("UPDATE RACE SET CURRENT_LAP=CURRENT_LAP+1 WHERE ID={};".format(i))               
                lock.release() 
                #display(data)

                #tk_display(table,data)

            

def scoreboarddisplay(lock,quit_val,log_lock,start_time,pause_timer,number_of_participants,number_of_laps):    
    db=custom_database.database("my_sql.db")
    def tk_display(tk_main_window,detail_table,rank_table,path,log_text_widget,log_lock,elapsed_time,current_leader,pause_timer):
        
        """ lock.acquire()
        with open(path,'r') as datafile:
            data=json.loads(datafile.read())
        lock.release()
         """
        #print(data)
        #print('#######################################################')
        result_detailed,result_ranked=my_sort(lock,db,number_of_laps) 
        temp_elapsed_time=0.00
        if start_time.value!=0.00:
            temp_elapsed_time=round(Decimal(time.time()-start_time.value),3)
        if quit_val.value==0:
            elapsed_time.configure(text='ELAPSED TIME\n{}\n(-{})'.format(temp_elapsed_time,round(Decimal(pause_timer.value),3)))
            tk_main_window.protocol("WM_DELETE_WINDOW", disable_event)
        else:
            tk_main_window.protocol("WM_DELETE_WINDOW", quit)

        detail_table_header=tuple(detail_table.get_row(0))
        rank_table_header=tuple(rank_table.get_row(0))
        result_detailed.insert(0,detail_table_header)    
        result_ranked.insert(0,rank_table_header)
        
        detail_table.update_values(result_detailed)
        rank_table.update_values(result_ranked)

        log_display(log_text_widget,log_lock)
        tk_main_window.after(1000, tk_display,tk_main_window, detail_table,rank_table,path,log_text_widget,log_lock,elapsed_time,current_leader,pause_timer)

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
    my_col_names_rank=('  RANK  ','  NAME  ',' CURRENT LAP ',' BEST LAP TIME ')
    my_col_names_detail=['  NAME  ']
    my_col_names_detail.extend(['  LAP {}  '.format(i+1) for i in range(number_of_laps)])
    my_col_names_detail=tuple(my_col_names_detail)
    
    
    my_table_rank = CTkTable.CTkTable(master=display_label,
                                     row=number_of_participants+1,
                                     column=len(my_col_names_rank),
                                     values=(my_col_names_rank,)
                                     )
    
    elapsed_time= customtkinter.CTkLabel(master=display_label,fg_color="transparent",text_color='green',justify='center')
    current_leader= customtkinter.CTkLabel(master=display_label,fg_color="transparent",text_color='orange',justify='center')

    my_table_detail = CTkTable.CTkTable(master=display_label,
                                       row=number_of_participants+1,
                                       column=len(my_col_names_detail),
                                       values=(my_col_names_detail,)
                                       )
        #2 info display table 
    race_current_stat=customtkinter.CTkTextbox(info_label,fg_color='transparent',text_color='red',
                        font=('Courier',10), wrap='word',
                        xscrollcommand=False,yscrollcommand=False,
                        )
    #packing
    for my_frame_number in range(len(root_widgets)):
        root_widgets[my_frame_number].grid(row=my_frame_number,column=0,sticky="nsew")

    ## inside display label
    my_table_rank.grid(row=0,column=0,rowspan=2,sticky='nsew',padx=10,pady=10)
    elapsed_time.grid(row=0,column=1,sticky='nsew',padx=10,pady=10)
    current_leader.grid(row=1,column=1,sticky='nsew',padx=10,pady=10)  
    my_table_detail.grid(row=2,column=0,columnspan=2,sticky='nsew',padx=10,pady=10)
        
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
    path=''
    tk_display(root,my_table_detail,my_table_rank,path,race_current_stat,log_lock,elapsed_time,current_leader,pause_timer)
    #log_display(race_current_stat,log_lock)
        
    #root.after(1, tk_display, table, data)
    root.mainloop()    




class formula_race():
    def __init__(self,number_of_laps,rfid_list: list):
        '''
        data = []
        for i in participant_name_list:
            d={'id':i , 'lap':0, 'score': [0.0]*(number_of_laps+1)}
            data.append(d)

        
        path='score.txt'

        with open(path,'w+') as datafile:
            json.dump(data,datafile)
        '''
        my_log.clearlogfile()
        my_log.write("Race STARTED")
        db=custom_database.database("my_sql.db")
        db.run('DROP TABLE IF EXISTS RACE;')
        #db.run("CREATE TABLE RACE(ID INT,RANK INT, NAME VARCHAR(100),TOTAL_LAP INT, CURRENT_LAP INT,  FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE NO ACTION) STRICT; ")
        db.run("CREATE TABLE RACE(ID INT,RANK INT, NAME TEXT,TOTAL_LAP INT, CURRENT_LAP INT,  FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE NO ACTION) STRICT; ")
        for i in range(number_of_laps+1):
            db.run("ALTER TABLE RACE ADD LAP{} REAL;".format(i+1))
        for i in rfid_list:
            temp_name=db.run("SELECT NAME FROM TEAMS WHERE ID={};".format(i))[0][0]
            temp_list=[str(i),'0',"'{}'".format(temp_name),'{}'.format(number_of_laps),'0'] 
            temp_list.extend(['0.0']*(number_of_laps+1))
            
            value_text=','.join(temp_list)
            db.run("INSERT INTO RACE VALUES({});".format(value_text))

        
        
        lock=multiprocessing.Lock()
        log_lock=multiprocessing.Lock()
        quit_val = multiprocessing.Value('i', 0)
        pause_timer=multiprocessing.Value('d',0.0)
        start_time=multiprocessing.Value('d',0.0)
                        
        processes = []

        p2 = multiprocessing.Process(target=scoreboardcalculation,args=(lock,quit_val,pause_timer,log_lock,start_time))
        p1 = multiprocessing.Process(target=scoreboarddisplay,args=(lock,quit_val,log_lock,start_time,pause_timer,len(rfid_list),number_of_laps))
        processes.append(p1)
        processes.append(p2)

        p1.start()
        p2.start()
        # Waiting for all processes to complete
        for p in processes:
            p.join()
        print("All tasks completed")

if __name__=='__main__':
    formula_race(6,[1,2])        