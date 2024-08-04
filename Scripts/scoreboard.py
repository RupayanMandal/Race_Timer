import time
import numpy as np
from operator import itemgetter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import time
import random
from threading import Thread
import multiprocessing
import keyboard
import json

#custom libraries
import tkinter_display as my_display
import my_log

display_on=True

def my_sort(data:dict):
    data=[{'id':i['id'],'lap':i['lap'],'score':i['score'][::-1]} for i in data]
    s=sorted(data,key=itemgetter('lap','score'),reverse=True)
    return list(map(itemgetter('id'),s))

def display(data: dict):
    sorted_order=my_sort(data)  
    for id in sorted_order:
        pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
        lap_text=' LAP -> {},  Rank - {}'.format(data[pos]['lap'],sorted_order.index(id)+1)
        #print(data[pos]['id'],' ',data[pos]['score'][0:6], lap_text)



def disable_event():
    pass


def scoreboardcalculation(lock,path,quit_val,pause_timer,log_lock):
    lock.acquire()
    with open(path,'r') as datafile:
        data=json.loads(datafile.read())
    lock.release()    
 
    obj = time.gmtime(0)
    paused=0
    start_time=0.0
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
        elif i=='p':
            paused=1-paused
            print(paused)
            if paused==1:
                msg="Race PAUSED"
                log_lock.acquire()
                my_log.write(msg)
                log_lock.release()
                
                if start_time==0.0:
                    start_time=time.time()
            elif paused==0:
                temp=max(0.0,time.time()-start_time)
                pause_timer_value=pause_timer.value
                pause_timer_value+=temp
                pause_timer.value=pause_timer_value
                start_time=0.0
                msg="Race RESUMED after a pause of {} seconds \n \t\t\t\tTotal pause time = {} seconds".format(temp,pause_timer_value)
                log_lock.acquire()
                my_log.write(msg)
                log_lock.release()
                print('+++++++++++++++++++++++++++++++++ ',pause_timer)
                        

        elif i not in list(map(itemgetter('id'),data)) and i!=0:
            continue 
        else:
            if not paused:
                i=data.index(list(filter(lambda data: data['id'] == i, data))[0])
                #print(i)
                if  data[i]['score'][6]!=0:
                    continue  
                    
                t=time.time()
                data[i]['score'][data[i]['lap']]=-t
                if data[i]['lap'] in range (1,7):
                    data[i]['score'][data[i]['lap']-1]=t-abs(data[i]['score'][data[i]['lap']-1])
                    msg="car {} has successfully completed lap {} in {} seconds ".format(data[i]['id'],
                                                                                         data[i]['lap'],
                                                                                         data[i]['score'][data[i]['lap']-1]           
                                                                                         )
                    log_lock.acquire()
                    my_log.write(msg)
                    log_lock.release()
                    
                    if data[i]['lap']==6:
                        print(sum(data[i]['score'][0:6]))
                        print(pause_timer.value)
                        data[i]['score'][6]=sum(data[i]['score'][0:6])-pause_timer.value
                        msg="car {} has successfully completed THE RACE in {} seconds ".format(data[i]['id'],
                                                                                         data[i]['score'][6]           
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

            

def scoreboarddisplay(lock,path,quit_val,log_lock):    

    def tk_display(tk_main_window,t,path,log_text_widget,log_lock):
        lock.acquire()
        with open(path,'r') as datafile:
            data=json.loads(datafile.read())
        lock.release()
        #print(data)
        #print('#######################################################')
        sorted_order=my_sort(data) 
        temp=1
        for id in sorted_order:
            pos=data.index(list(filter(lambda data: data['id'] == id, data))[0])
            display_arr=[sorted_order.index(id)+1, data[pos]['id']]
            display_arr.extend([max(i,0) for i in data[pos]['score']])
            #print(display_arr)
            t.update_row(row=temp,array=display_arr)
            temp+=1
        if quit_val.value==0:
            tk_main_window.protocol("WM_DELETE_WINDOW", disable_event)
        else:
            tk_main_window.protocol("WM_DELETE_WINDOW", quit)
        
        log_display(log_text_widget,log_lock)
        tk_main_window.after(3, tk_display,tk_main_window, table,path,log_text_widget,log_lock)

    def log_display(text_widget,log_lock):
        
        log_lock.acquire()
        msg=my_log.read()
        log_lock.release()
        #text_widget.config(state='normal')
        text_widget.delete(1.0,END)
        text_widget.insert(END,msg) 
        text_widget.yview(END)
        #text_widget.config(state='disabled')   

    
    root = Tk()
    root_widgets=[]
    
    #root widgets
    display_label_name=Label(root,padx=10,foreground='Black',font=('Courier',18,'bold'),text='SCORE BOARD',justify='left')
    root_widgets.append(display_label_name)
    
    display_label=Frame(root,padx=10,pady=10)
    root_widgets.append(display_label)
    
    info_label_name=Label(root,padx=10,foreground='Black',font=('Courier',18,'bold'),text='LOG',justify='left')
    root_widgets.append(info_label_name)

    info_label=Frame(root)
    root_widgets.append(info_label)
    
    
    
    
    #widgets
        #1. score display table
    my_col_names=['  RANK  ','  ID  ','  LAP 1  ','  LAP 2  ','  LAP 3  ','  LAP 4  ','  LAP 5  ','  LAP 6  ',' Total Time']
    table = my_display.Table(display_label,rows=7,cols=len(my_col_names),col_names=my_col_names)
        #2 info display table 
    race_current_stat=Text(info_label,background='white',foreground='red',
                           font=('Courier',10), wrap='word',
                           xscrollcommand=False,yscrollcommand=False,
                           )
    #packing
    for my_frame_number in range(len(root_widgets)):
        root_widgets[my_frame_number].grid(row=my_frame_number,column=0,sticky="nsew")
        
    ## inside info label
    race_current_stat.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)
    
    #row and column configure
    root.rowconfigure(list(range(len(root_widgets))),weight=1)
    root.columnconfigure(0,weight=1)
    for i in root_widgets:
        if not isinstance(i,Frame):
            continue
        col,row=i.grid_size()
        i.rowconfigure(list(range(row)),weight=1)
        i.columnconfigure(list(range(col)),weight=1)
        
    
    #table.update(1,4,'Hello')
    tk_display(root,table,path,race_current_stat,log_lock)
    #log_display(race_current_stat,log_lock)
           
    #root.after(1, tk_display, table, data)
    root.mainloop()    


laps=6
number_of_participants=6
data = []

for i in range(1,number_of_participants+1):
    d={'id':i , 'lap':0, 'score': [0.0]*(laps+1)}
    data.append(d)


if __name__=='__main__':
    my_log.clearlogfile()
    my_log.write("Race STARTED")
    path='score.txt'

    with open(path,'w+') as datafile:
        json.dump(data,datafile)
    
    
    lock=multiprocessing.Lock()
    log_lock=multiprocessing.Lock()
    quit_val = multiprocessing.Value('i', 0)
    pause_timer=multiprocessing.Value('d',0.0)
                    
    processes = []

    p1 = multiprocessing.Process(target=scoreboardcalculation,args=(lock,path,quit_val,pause_timer,log_lock))
    p2 = multiprocessing.Process(target=scoreboarddisplay,args=(lock,path,quit_val,log_lock))
    processes.append(p1)
    processes.append(p2)

    p1.start()
    p2.start()
    # Waiting for all processes to complete
    for p in processes:
        p.join()
    print("All tasks completed")