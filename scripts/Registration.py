import tkinter.messagebox
import customtkinter
import CTkTable
import tkinter
import custom_database
class add():
    def __init__(self,frame,db,*args,**kwargs):
        self.frame=frame
        self.frame.columnconfigure([0,1,2],weight=1)
        self.set_frame()
        self.db=db
        #self.db.run("CREATE TABLE IF NOT EXISTS TEAMS (ID INT PRIMARY KEY, NAME VARCHAR(100) UNIQUE);")
        #self.db.run("CREATE TABLE IF NOT EXISTS MEMBERS (ID INT , NAME VARCHAR(100) CONSTRAINT fk_ID FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE CASCADE);")

    def set_frame(self):    
        team_frame=customtkinter.CTkFrame(master=self.frame)
        team_frame.columnconfigure([0,1,2],weight=1)
        rfid_number_label=customtkinter.CTkLabel(master=self.frame,text='RFID NUMBER',anchor='e')
        rfid_number=customtkinter.CTkEntry(master=self.frame,fg_color='transparent',placeholder_text='Your RFID TAG id will show here')
        rfid_lock=customtkinter.CTkButton(master=self.frame,text='Lock',command=lambda:self.Lock_rfid(rfid_lock,rfid_number,team_frame))
        
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
        team_frame.grid(row=1,column=0,columnspan=3,sticky='nsew')

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
    
    def Lock_rfid(self,calling_btn,rfid_number,team_frame):
        print(rfid_number.get())
        ids=self.db.run("SELECT * from TEAMS WHERE ID={}".format(int(rfid_number.get())))
        print(ids)
        if ids==[]: 
            rfid_number.configure(state='disabled')
            self.enable_children(team_frame.winfo_children())
            calling_btn.configure(state='disabled')

        else:
            tkinter.messagebox.showerror("ERROR","RFID number {} has already been assignted to Team {}\nPlease Try Again with a different RFID".format(ids[0][0],ids[0][1]))    
        

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
    def __init__(self,frame,db,*args,**kwargs):
        self.frame=frame
        self.frame.columnconfigure([0,1,2],weight=1)
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
        clr_btn=customtkinter.CTkButton(master=self.frame,height=100,text='CLEAR',font=('courier',18,'bold'),state='normal',command=self.clear_frame)

        
        
        
        #main frame
        team_name_label.grid(row=0,column=0,sticky='ew',padx=10,pady=(50,10))
        team_name.grid(row=0,column=1,sticky='ew',padx=10,pady=(50,10))
        member_name_label.grid(row=1,column=0,sticky='ew',padx=10,pady=(20,0))
        self.member_name.grid(row=1,column=1,sticky='ew',padx=10,pady=(20,0))
        
        self.remove_btn.grid(row=2,column=0,sticky='nsew',padx=5,pady=(40,10))
        clr_btn.grid(row=2,column=1,sticky='nsew',padx=5,pady=(40,10))

    
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
    
    
class registration():
    def __init__(self):
        self.team_list=[]
        self.db=custom_database.database("my_sql.db")
        self.db.run("CREATE TABLE IF NOT EXISTS TEAMS (ID INT PRIMARY KEY, NAME VARCHAR(100) UNIQUE);")
        self.db.run("CREATE TABLE IF NOT EXISTS MEMBERS (ID INT , NAME VARCHAR(100) ,FOREIGN KEY (ID) REFERENCES TEAMS(ID) ON DELETE CASCADE);")

        self.root=customtkinter.CTk()
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure([0,1],weight=1)
        left_tabview = customtkinter.CTkTabview(master=self.root)
        left_tabview.add("ADD")  # add tab at the end
        left_tabview.add("REMOVE")  # add tab at the end
        left_tabview.add("VIEW")
        left_tabview.set("ADD") 
        
        add(frame=left_tabview.tab("ADD"),db=self.db)
        remove(frame=left_tabview.tab("REMOVE"),db=self.db)


        left_tabview.grid(row=0,column=0,sticky='nsew',padx=(10,0))
        
        right_tabview = customtkinter.CTkTabview(master=self.root)
        right_tabview.add("TEAMS")  # add tab at the end
        right_tabview.tab('TEAMS').columnconfigure(0,weight=1)
        right_tabview.tab('TEAMS').rowconfigure(2,weight=1)
        right_tabview.add("MEMBERS")  # add tab at the end
        right_tabview.tab('MEMBERS').columnconfigure(0,weight=1)
        right_tabview.tab('MEMBERS').rowconfigure(2,weight=1)
        right_tabview.set("TEAMS") 

        right_tabview.grid(row=0,column=1,sticky='nsew',padx=(10,0))
        
        scrollable_team_frame=customtkinter.CTkScrollableFrame(master=right_tabview.tab('TEAMS'))
        scrollable_team_frame.columnconfigure(0,weight=1)
        scrollable_team_frame.grid(row=2,column=0,sticky='nsew',padx=20,pady=20)
        self.team_table_view=CTkTable.CTkTable(master=scrollable_team_frame,row=1,column=2,values=[['RFID','NAME']])
        self.team_table_view.grid(row=0,column=0,sticky='ew',padx=20,pady=10)

        self.update_team_table_btn=customtkinter.CTkButton(master=right_tabview.tab('TEAMS'),text='\nREFRESH\n',command=lambda:self.update_view_team(self.team_table_view,self.count_team_table_label))
        self.update_team_table_btn.grid(row=0,column=0,sticky='ew',padx=20,pady=(50,0))

        self.count_team_table_label=customtkinter.CTkLabel(master=right_tabview.tab('TEAMS'))
        self.count_team_table_label.grid(row=1,column=0,sticky='ew',padx=20,pady=(30,0))

        scrollable_member_frame=customtkinter.CTkScrollableFrame(master=right_tabview.tab('MEMBERS'))
        scrollable_member_frame.columnconfigure(0,weight=1)
        scrollable_member_frame.grid(row=2,column=0,sticky='nsew',padx=20,pady=20)


        self.member_table_view=CTkTable.CTkTable(master=scrollable_member_frame,row=1,column=2,values=[['RFID','NAME']])
        self.member_table_view.grid(row=0,column=0,sticky='ew',padx=20,pady=10)

        self.update_member_table_btn=customtkinter.CTkButton(master=right_tabview.tab('MEMBERS'),text='\nREFRESH\n',command=lambda:self.update_view_member(self.member_table_view,self.count_member_table_label))
        self.update_member_table_btn.grid(row=0,column=0,sticky='ew',padx=20,pady=(50,0))

        self.count_member_table_label=customtkinter.CTkLabel(master=right_tabview.tab('MEMBERS'))
        self.count_member_table_label.grid(row=1,column=0,sticky='ew',padx=20,pady=(30,0))



        self.update_view_team(self.team_table_view,self.count_team_table_label)
        self.update_view_member(self.member_table_view,self.count_member_table_label)
        self.root.mainloop()
    
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
    registration()        