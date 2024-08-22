import tkinter.messagebox
import customtkinter
import CTkTable
import tkinter
import custom_database
import toggle_button
import RFID_time_trial as time_trial
import RFID_formula as formula

import custom_rfid_scan_dialog_box
import threading
import serial

class serial_listener(threading.Thread):
    def __init__(self):
        # execute the base constructor
        threading.Thread.__init__(self)
        # set a default value
        self.value = ''
    def run(self):
        try:
            serial_port=serial.Serial(port="COM6",baudrate=9600)
            temp=str(serial_port.readline())
            temp=str(serial_port.readline())
            temp=''.join([i for i in temp if i.isdigit()])
            data=int(temp)
            if data!='' and data!=' ':
                self.value=int(temp)

        except Exception as e:
            tkinter.messagebox.showerror(title="RFID dialogue ERROR", message=e)
            print(e)      

class add():
    def __init__(self,root,frame,db,*args,**kwargs):
        self.root=root
        self.frame=frame
        self.frame.columnconfigure([0,1,2,3],weight=1)
        self.set_frame()
        self.db=db
        #self.db.run("CREATE TABLE IF NOT EXISTS TEAMS (ID INT PRIMARY KEY, NAME VARCHAR(100) UNIQUE);")
        #self.db.run("CREATE TABLE IF NOT EXISTS MEMBERS (ID INT , NAME VARCHAR(100) CONSTRAINT fk_ID FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE CASCADE);")

    def set_frame(self):    
        team_frame=customtkinter.CTkFrame(master=self.frame)
        team_frame.columnconfigure([0,1,2],weight=1)
        rfid_number_label=customtkinter.CTkLabel(master=self.frame,text='RFID NUMBER',anchor='e')
        rfid_number=customtkinter.CTkEntry(master=self.frame,fg_color='transparent',placeholder_text='Your RFID TAG id will show here')
        rfid_number.delete(0,'end')
        rfid_number.insert(0,'Press Scan to start')
        rfid_number.configure(state='readonly')
        rfid_lock=customtkinter.CTkButton(master=self.frame,text='Lock',state='disabled',command=lambda:self.Lock_rfid(rfid_lock,rfid_number,team_frame))
        rfid_scan=customtkinter.CTkButton(master=self.frame,text='Scan',command=lambda:self.scan_rfid(entry_field=rfid_number,lock_button=rfid_lock))
        
        team_name_label=customtkinter.CTkLabel(master=team_frame,text='TEAM NAME')
        team_name=customtkinter.CTkEntry(master=team_frame,fg_color='transparent',placeholder_text='Enter your team name',state='disabled')

        
        number_of_member_label=customtkinter.CTkLabel(master=team_frame,text='NUMBER OF MEMBERS')
        number_of_member=customtkinter.CTkComboBox(master=team_frame, values=["1","2","3","4"],
                                                    command=self.combobox_callback,state='readonly')

        
        member_label=customtkinter.CTkLabel(master=team_frame,text="MEMBERS' NAMES")
        self.member_frame=customtkinter.CTkFrame(master=team_frame,)
        self.member_entry_list=[]

        add_btn=customtkinter.CTkButton(master=team_frame,height=100,text='ADD TEAM',font=('courier',18,'bold'),state='disabled',command=lambda: self.add_teams(rfid_number,team_name))
        clr_btn=customtkinter.CTkButton(master=team_frame,height=100,text='CLEAR',font=('courier',18,'bold'),state='disabled',command=self.clear_frame)

        #main frame
        rfid_number_label.grid(row=0,column=0,sticky='ew',padx=5,pady=(50,10))
        rfid_number.grid(row=0,column=1,sticky='ew',padx=5,pady=(50,10))
        rfid_lock.grid(row=0,column=2,sticky='ew',padx=5,pady=(50,10))
        rfid_scan.grid(row=0,column=3,sticky='ew',padx=5,pady=(50,10))
        team_frame.grid(row=1,column=0,columnspan=4,sticky='nsew')

        ##TEAM FRAME
        team_name_label.grid(row=0,column=0,sticky='ew',padx=5,pady=10)
        team_name.grid(row=0,column=1,sticky='ew',padx=5,pady=10)
        number_of_member_label.grid(row=1,column=0,sticky='ew',padx=5,pady=10)
        number_of_member.grid(row=1,column=1,sticky='ew',padx=5,pady=10)
        member_label.grid(row=2,column=0,sticky='ew',padx=5,pady=10)
        self.member_frame.grid(row=2,column=1,columnspan=2,sticky='ew',padx=5,pady=10)
        add_btn.grid(row=3,column=1,sticky='nsew',padx=5,pady=(30,10))
        clr_btn.grid(row=3,column=2,sticky='nsew',padx=5,pady=(30,10))

    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.set_frame()

    def enable_children(self,children):
        for child in children :
            if isinstance(child,customtkinter.CTkEntry) or isinstance(child,customtkinter.CTkButton):
                print(child)
                child.configure(state='normal')
    
    def scan_rfid(self,entry_field,lock_button):
        rfid=custom_rfid_scan_dialog_box.RFIDScannerDialog(text='Scanning.....', title='Scanning for RFID')
        #rfid=custom_rfid_scan_dialog_box.start()
        print(rfid.get_input())
        if rfid.data!='' and rfid.data!=' ':
            
            entry_field.configure(state='normal')
            entry_field.delete(0,'end')
            entry_field.insert(0,rfid.data)
            entry_field.configure(state='readonly')
            lock_button.configure(state='normal')
        else:
            entry_field.configure(state='normal')
            entry_field.delete(0,'end')
            entry_field.insert(0,'No RFID FOUND')
            entry_field.configure(state='readonly')
            lock_button.configure(state='disabled')


    def Lock_rfid(self,calling_btn,rfid_number,team_frame):
        try:
            rfid_id=int(rfid_number.get())
            ids=self.db.run("SELECT * from TEAMS WHERE ID={}".format(rfid_id))
            if ids==[]: 
                rfid_number.configure(state='disabled')
                self.enable_children(team_frame.winfo_children())
                calling_btn.configure(state='disabled')

            else:
                tkinter.messagebox.showerror("ERROR","RFID number {} has already been assignted to Team {}\nPlease Try Again with a different RFID".format(ids[0][0],ids[0][1]))    
        

        except:
            pass
        
    def combobox_callback(self,choice):
        print("combobox dropdown clicked:", choice)
        member_number=int(choice)
        self.member_entry_list=[]
        for i in range(member_number):
            mem_num_label=customtkinter.CTkLabel(master=self.member_frame,fg_color='transparent',text=i+1,anchor='w')
            mem_entry=customtkinter.CTkEntry(master=self.member_frame,fg_color='gray80',text_color='black')
            
            mem_num_label.grid(row=i,column=0,sticky='ew',padx=5)
            mem_entry.grid(row=i,column=1,sticky='ew',padx=5)
            self.member_entry_list.append(mem_entry)

    def add_teams(self,rfid_number,team_name):
        confirm=tkinter.messagebox.askyesno(title='Confirm Add', message="Do You want to add Team '{}' to the team list ?".format(team_name.get()))
        if confirm:
            temp_team_name=team_name.get()
            ids=self.db.run("SELECT * FROM TEAMS WHERE NAME='{}';".format(temp_team_name))
            print(ids)
            if ids==[]:
                self.db.run("INSERT INTO TEAMS VALUES({},'{}');".format(int(rfid_number.get()),team_name.get()))
            else:
                tkinter.messagebox.showerror('ERROR',"RFID number {} has already been assignted to Team {}\nPlease Try Again with an different TEAM NAME".format(int(ids[0][0]),ids[0][1]))    
                
            print(self.member_entry_list)
            for i in self.member_entry_list:
                self.db.run("INSERT INTO MEMBERS VALUES({},'{}');".format(rfid_number.get(),i.get()))
            self.clear_frame()
            
class remove():
    def __init__(self,root,frame,db,*args,**kwargs):
        self.root=root
        self.frame=frame
        self.frame.columnconfigure([0,1,2,3],weight=1)
        self.db=db
        self.set_frame()
        
    def set_frame(self):
        teams=self.db.run("SELECT NAME FROM TEAMS")    
        teams=[i[0] for i in teams ]
        team_name_label=customtkinter.CTkLabel(master=self.frame,text='TEAM NAME',anchor='e')
        team_name=customtkinter.CTkComboBox(master=self.frame, values=teams,
                                                    command=self.team_combobox_callback,state='readonly')
        
        member_name_label=customtkinter.CTkLabel(master=self.frame,text='MEMBERS NAME',anchor='e')
        self.member_name=customtkinter.CTkComboBox(master=self.frame,
                                                   command=self.member_combobox_callback,
                                                    state='disabled')
        
        
        self.remove_btn=customtkinter.CTkButton(master=self.frame,height=100,text='REMOVE TEAM',font=('courier',18,'bold'),state='disabled',command=lambda: self.remove_teams(team_name.get(),self.member_name.get()))
        clr_btn=customtkinter.CTkButton(master=self.frame,height=100,text='CLEAR',font=('courier',20,'bold'),state='normal',command=self.clear_frame)

        
        
        
        #main frame
        team_name_label.grid(row=0,column=0,columnspan=2,sticky='ew',padx=10,pady=(50,10))
        team_name.grid(row=0,column=2,sticky='ew',padx=10,pady=(50,10))
        member_name_label.grid(row=1,column=0,columnspan=2,sticky='ew',padx=10,pady=(20,0))
        self.member_name.grid(row=1,column=2,sticky='ew',padx=10,pady=(20,0))
        
        self.remove_btn.grid(row=2,column=0,columnspan=2,sticky='nsew',padx=5,pady=(40,10))
        clr_btn.grid(row=2,column=2,columnspan=2,sticky='nsew',padx=5,pady=(40,10))

    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.set_frame()

    def team_combobox_callback(self,choice):
        temp_members=self.db.run("SELECT m.NAME FROM TEAMS t INNER JOIN MEMBERS m on t.ID=m.ID WHERE t.NAME='{}' ORDER BY m.NAME ;".format(choice))    
        members=['ALL']
        members.extend([i[0] for i in temp_members ])
        self.member_name.configure(state='readonly',values=members)
        self.member_name.set('Select members to be removed')

    def member_combobox_callback(self,choice):
        self.remove_btn.configure(state='normal')    

    def remove_teams(self,team_name,member_name):
        choice=tkinter.messagebox.askyesno("CONFIRM REMOVE","Do you want to remove {} from Team {} ?".format(member_name,team_name))
        if choice:
            total_member=self.db.run("SELECT COUNT(*) FROM TEAMS t INNER JOIN MEMBERS m ON t.ID=m.ID WHERE t.NAME='{}';".format(team_name))
            
            if total_member[0]==(1,):
                member_name='ALL'
            else:
                pass    
            if member_name=='ALL':
                x=self.db.run("DELETE FROM TEAMS WHERE NAME='{}';".format(team_name))
            else:
                self.db.run("DELETE FROM MEMBERS WHERE NAME='{}';".format(member_name))
        self.clear_frame()        

class race():
    def __init__(self,root,frame,db,*args,**kwargs):
        self.root=root
        self.frame=frame
        self.frame.columnconfigure([0,1],weight=1)
        self.db=db
        self.set_frame()
        
        #self.db.run("CREATE TABLE IF NOT EXISTS TEAMS (ID INT PRIMARY KEY, NAME VARCHAR(100) UNIQUE);")
        #self.db.run("CREATE TABLE IF NOT EXISTS MEMBERS (ID INT , NAME VARCHAR(100) CONSTRAINT fk_ID FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE CASCADE);")

    def set_frame(self):    
        
        race_type_label=customtkinter.CTkLabel(master=self.frame,text='RACE TYPE',fg_color='transparent')
        race_type_button_frame=customtkinter.CTkFrame(master=self.frame,fg_color='transparent')
        race_type_button_frame.columnconfigure([0,1],weight=1)
        self.race_buttons=toggle_button.toggle_button(master_frame=race_type_button_frame,
                                                display_texts=['FORMULA','TIME TRIAL'],
                                                default='TIME TRIAL',
                                                resize=True)
        add_team_label=customtkinter.CTkLabel(master=self.frame,text='CURRENT TEAMS')
        checkbox_frame=customtkinter.CTkScrollableFrame(master=self.frame)
        checkbox_frame.columnconfigure([0,1,2],weight=1)
        name_list=self.db.run('SELECT NAME FROM TEAMS;')
        
        i,j=0,0
        for name in name_list:
            check_var = customtkinter.StringVar(value=name[0])  
            checkbox = customtkinter.CTkCheckBox(master=checkbox_frame, text=name[0], 
                                     variable=check_var, onvalue=name[0], offvalue="off")
            
            checkbox.grid(row=i,column=j,sticky='ew',padx=10,pady=10)
            j+=1
            if j>0:
                j=0
                i+=1
                
        add_btn=customtkinter.CTkButton(master=self.frame,height=100,text='START RACE',font=('courier',18,'bold'),state='normal',command=lambda: self.add_teams_checkbox(add_btn,checkbox_frame))
        clr_btn=customtkinter.CTkButton(master=self.frame,height=100,text='RESET',font=('courier',18,'bold'),state='normal',command=self.clear_frame)

        #main frame
        race_type_label.grid(row=0,column=0,sticky='ew',padx=5,pady=(50,10))
        race_type_button_frame.grid(row=0,column=1,sticky='ew',padx=5,pady=(50,10))
        add_team_label.grid(row=1,column=0,sticky='ew',padx=5,pady=(10,10))
        checkbox_frame.grid(row=1,column=1,sticky='ew',padx=5,pady=(10,10))
        add_btn.grid(row=2,column=0,sticky='ew',padx=5,pady=5)
        clr_btn.grid(row=2,column=1,sticky='ew',padx=5,pady=5)
        
    def add_teams_checkbox(self,add_btn,checkbox_frame):
        lapdialogue=customtkinter.CTkInputDialog(text='Enter number of laps')
        laps=lapdialogue.get_input()
        comdialogue=customtkinter.CTkInputDialog(text='Enter com port')
        comport=comdialogue.get_input()
        
        try:
            laps=int(laps)
            comport=int(comport)
            s=serial.Serial(port="COM{}".format(comport),baudrate=9600)
            s.close()
        except Exception as e:
            tkinter.messagebox.showerror('COM PORT ERROR',e)
            return    
        add_btn.configure(state='disabled')
        name_list=[]
        race_type=self.race_buttons.selected_text
        for i in checkbox_frame.winfo_children():
            print(i,i.get())
            if isinstance(i,customtkinter.CTkCheckBox) and i.get()!='off':
                name_list.append(i.get())
        print(name_list)
        rfid_list=[]
        for name in name_list:
            rfid=self.db.run("SELECT ID FROM TEAMS WHERE NAME='{}'".format(name))[0][0]
            rfid_list.append(rfid)
        print(rfid_list)
        if race_type=='TIME TRIAL':
            time_trial.time_trial_race(com_port=comport,number_of_laps=laps,participant_name_list=rfid_list)
        elif race_type=='FORMULA':
            formula.formula_race(com_port=comport,number_of_laps=laps,participant_name_list=rfid_list)    

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.set_frame()

class view():
    def __init__(self,root,frame,db,*args,**kwargs):
        self.root=root
        self.frame=frame
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure([0,1,2],weight=1)
        self.set_frame()
        self.db=db
        #self.db.run("CREATE TABLE IF NOT EXISTS TEAMS (ID INT PRIMARY KEY, NAME VARCHAR(100) UNIQUE);")
        #self.db.run("CREATE TABLE IF NOT EXISTS MEMBERS (ID INT , NAME VARCHAR(100) CONSTRAINT fk_ID FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE CASCADE);")

    def set_frame(self):    
        self.rfid_scan=customtkinter.CTkButton(master=self.frame,text='Scan',command=self.show_rfid)
        self.rfid_label=customtkinter.CTkLabel(master=self.frame,text='HELLO',anchor='center')
        self.rfid_scan.grid(row=0,column=1,sticky='nsew',padx=5,pady=(50,10))
        self.rfid_label.grid(row=2,column=1,sticky='nsew',padx=5,pady=(50,10))
    
    
    def show_rfid(self):
        self.rfid_scan.configure(text='Please Wait\nScanning..',state='disabled')
        rfid=custom_rfid_scan_dialog_box.RFIDScannerDialog(text='Scanning.....', title='Scanning for RFID')
        
        #rfid=custom_rfid_scan_dialog_box.start()
        id=rfid.get_input()
        if id!='' and id!=' ':
            try:
                team=self.db.run("SELECT NAME from TEAMS where id={}".format(id))
                print(team)
                if team==[]:
                    info_msg='RFID: {}\n\n NEW RFID FOUND\n\nNO TEAM ASSIGNED TO {}'.format(id,id)                                               
                
                else:
                    mem=self.db.run("SELECT m.NAME FROM TEAMS t INNER JOIN MEMBERS m ON t.ID=m.ID where t.ID={} ORDER BY m.NAME ASC;".format(id))
                    mem_text='\n'
                    t=1
                    for i in mem:
                        mem_text=mem_text+' '*4+str(t)+". "+i[0]+'\n'
                        t+=1
                    info_msg='TEAM: {}\n\n  RFID: {}\n\nMEMBERS.... {}'.format(team[0][0],
                                                                        id,
                                                                        mem_text)
                self.rfid_label.configure(text=info_msg)
                    
            except:
                pass
        else:
            self.rfid_label.configure(text='NO RFID FOUND')

        self.rfid_scan.configure(text='Scan',state='normal')    
        
    def Lock_rfid(self,calling_btn,rfid_number,team_frame):
        try:
            rfid_id=int(rfid_number.get())
            ids=self.db.run("SELECT * from TEAMS WHERE ID={}".format(rfid_id))
            if ids==[]: 
                rfid_number.configure(state='disabled')
                self.enable_children(team_frame.winfo_children())
                calling_btn.configure(state='disabled')

            else:
                tkinter.messagebox.showerror("ERROR","RFID number {} has already been assignted to Team {}\nPlease Try Again with a different RFID".format(ids[0][0],ids[0][1]))    
        

        except:
            pass
        
    def combobox_callback(self,choice):
        print("combobox dropdown clicked:", choice)
        member_number=int(choice)
        self.member_entry_list=[]
        for i in range(member_number):
            mem_num_label=customtkinter.CTkLabel(master=self.member_frame,fg_color='transparent',text=i+1,anchor='w')
            mem_entry=customtkinter.CTkEntry(master=self.member_frame,fg_color='gray80',text_color='black')
            
            mem_num_label.grid(row=i,column=0,sticky='ew',padx=5)
            mem_entry.grid(row=i,column=1,sticky='ew',padx=5)
            self.member_entry_list.append(mem_entry)

    def add_teams(self,rfid_number,team_name):
        confirm=tkinter.messagebox.askyesno(title='Confirm Add', message="Do You want to add Team '{}' to the team list ?".format(team_name.get()))
        if confirm:
            temp_team_name=team_name.get()
            ids=self.db.run("SELECT * FROM TEAMS WHERE NAME='{}';".format(temp_team_name))
            print(ids)
            if ids==[]:
                self.db.run("INSERT INTO TEAMS VALUES({},'{}');".format(int(rfid_number.get()),team_name.get()))
            else:
                tkinter.messagebox.showerror('ERROR',"RFID number {} has already been assignted to Team {}\nPlease Try Again with an different TEAM NAME".format(int(ids[0][0]),ids[0][1]))    
                
            print(self.member_entry_list)
            for i in self.member_entry_list:
                self.db.run("INSERT INTO MEMBERS VALUES({},'{}');".format(rfid_number.get(),i.get()))
            self.clear_frame()

    
class registration():
    def __init__(self):
        self.team_list=[]
        self.db=custom_database.database("my_sql.db")
        self.db.run("CREATE TABLE IF NOT EXISTS TEAMS (ID INT PRIMARY KEY, NAME VARCHAR(100) UNIQUE);")
        self.db.run("CREATE TABLE IF NOT EXISTS MEMBERS (ID INT , NAME VARCHAR(100) ,FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE CASCADE);")

        self.root=customtkinter.CTk()
        self.root.title('Registration Window')
        self.root.rowconfigure(1,weight=1)
        self.root.columnconfigure([0,1,2],weight=1)
        toggle_button_frame=customtkinter.CTkFrame(self.root,fg_color='transparent')
        working_area_frame=customtkinter.CTkScrollableFrame(self.root)

        toggle_button.toggle_button(master_frame=toggle_button_frame,
                                    display_frame=working_area_frame,
                                    display_texts=['ADD','REMOVE','RACE','VIEW'],
                                    event_list=(
                                                (add,self.root,working_area_frame,self.db),
                                                (remove,self.root,working_area_frame,self.db),
                                                (race,self.root,working_area_frame,self.db),
                                                (view,self.root,working_area_frame,self.db)),
                                    default='ADD',
                                    resize=True            
                                    )
        #remove(frame=left_tabview.tab("REMOVE"),db=self.db)


        toggle_button_frame.grid(row=0,column=0,columnspan=2,sticky='ew',padx=(10,0),pady=(50,0))
        working_area_frame.grid(row=1,column=0,columnspan=2,sticky='nsew',padx=(10,0),pady=(20,20))
        
        right_tabview = customtkinter.CTkTabview(master=self.root)
        
        right_tabview.add("TEAMS")  # add tab at the end
        right_tabview.tab('TEAMS').columnconfigure(0,weight=1)
        right_tabview.tab('TEAMS').rowconfigure(2,weight=1)
        right_tabview.add("MEMBERS")  # add tab at the end
        right_tabview.tab('MEMBERS').columnconfigure(0,weight=1)
        right_tabview.tab('MEMBERS').rowconfigure(2,weight=1)
        right_tabview.set("TEAMS") 

        right_tabview.grid(row=0,column=2,sticky='nsew',rowspan=2,padx=(10,0))
        
        scrollable_team_frame=customtkinter.CTkScrollableFrame(master=right_tabview.tab('TEAMS'))
        scrollable_team_frame.columnconfigure(0,weight=1)
        scrollable_team_frame.grid(row=2,column=0,sticky='nsew',padx=20,pady=20)
        self.team_table_view=CTkTable.CTkTable(master=scrollable_team_frame,
                                               row=1,
                                               column=2,
                                               values=[['RFID','NAME']],
                                               wraplength=200,
                                               hover_color='blue',
                                               command=self.clicked_team,
                                               )
        self.team_table_view.grid(row=0,column=0,sticky='ew',padx=20,pady=10)

        self.update_team_table_btn=customtkinter.CTkButton(master=right_tabview.tab('TEAMS'),text='\nREFRESH\n',command=lambda:self.update_view_team(self.team_table_view,self.count_team_table_label))
        self.update_team_table_btn.grid(row=0,column=0,sticky='ew',padx=20,pady=(50,0))

        self.count_team_table_label=customtkinter.CTkLabel(master=right_tabview.tab('TEAMS'))
        self.count_team_table_label.grid(row=1,column=0,sticky='ew',padx=20,pady=(30,0))

        scrollable_member_frame=customtkinter.CTkScrollableFrame(master=right_tabview.tab('MEMBERS'))
        scrollable_member_frame.columnconfigure(0,weight=1)
        scrollable_member_frame.grid(row=2,column=0,sticky='nsew',padx=20,pady=20)


        self.member_table_view=CTkTable.CTkTable(master=scrollable_member_frame,
                                                 row=1,
                                                 column=2,
                                                 values=[['TEAM','NAME']])
        self.member_table_view.grid(row=0,column=0,sticky='ew',padx=20,pady=10)

        self.update_member_table_btn=customtkinter.CTkButton(master=right_tabview.tab('MEMBERS'),text='\nREFRESH\n',command=lambda:self.update_view_member(self.member_table_view,self.count_member_table_label))
        self.update_member_table_btn.grid(row=0,column=0,sticky='ew',padx=20,pady=(50,0))

        self.count_member_table_label=customtkinter.CTkLabel(master=right_tabview.tab('MEMBERS'))
        self.count_member_table_label.grid(row=1,column=0,sticky='ew',padx=20,pady=(30,0))



        self.update_view_team(self.team_table_view,self.count_team_table_label)
        self.update_view_member(self.member_table_view,self.count_member_table_label)
        self.root.mainloop()
    
    def clicked_team(self,info):
        if info['row']!=0 and info['column']!=0:
            try:
                mem=self.db.run("SELECT m.NAME FROM TEAMS t INNER JOIN MEMBERS m ON t.ID=m.ID where t.NAME='{}' ORDER BY m.NAME ASC;".format(info['value']))
                mem_text='\n'
                t=1
                for i in mem:
                    mem_text=mem_text+' '*4+str(t)+". "+i[0]+'\n'
                    t+=1
                info_msg='TEAM: {}\n\n  RFID: {}\n\nMEMBERS.... {}'.format(info['value'],
                                                                    self.team_table_view.get(row=info['row'],column=0),
                                                                    mem_text)
                tkinter.messagebox.showinfo("TEAM INFO".format(info['value']),info_msg)
            except:
                pass    
    def update_view_team(self,team_table,total_label):
        rows=len(team_table.get())
        if rows==2:
            team_table.delete_row(1)
        elif rows>2:
            team_table.delete_rows(list(range(1,rows)))
        teams=self.db.run("SELECT * FROM TEAMS ORDER BY ID ASC")
        for i in range(len(teams)):
            team_table.add_row(values=teams[i])
        total_label.configure(text='TOTAL NUMBER OF TEAMS: {}'.format(len(teams)))     

    def update_view_member(self,table,total_label):
        rows=len(table.get())
        if rows==2:
            table.delete_row(1)
        elif rows>2:
            table.delete_rows(list(range(1,rows)))
        teams=self.db.run("SELECT t.name,m.name FROM TEAMS t INNER JOIN MEMBERS m ON t.ID=m.ID ORDER BY t.NAME ASC")
        temp_teams=[]
        display_tuple=()
        for i in range(len(teams)):
            if teams[i][0] not in temp_teams:
                temp_teams.append(teams[i][0])
                display_tuple=(teams[i][0],teams[i][1])
            else :
                display_tuple=('',teams[i][1])    
            table.add_row(values=display_tuple)                 
        total_label.configure(text='TOTAL NUMBER OF PARTICIPANTS: {}'.format(len(teams)))
                

if __name__=='__main__':
    customtkinter.set_default_color_theme("dark-blue")
    registration()        