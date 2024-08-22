import customtkinter
import CTkTable
import tkinter
import toggle_button
        

    
class selection_app():
    def __init__(self):
        root=customtkinter.CTk()
        self.team_name_list=[]
        frame_list=[]
        #widgets
        self.root_left_frame=customtkinter.CTkFrame(master=root,fg_color='transparent')
        root_right_frame=customtkinter.CTkFrame(master=root,fg_color='transparent')        
        
        ##LEFT frame
        race_type_label=customtkinter.CTkLabel(master=self.root_left_frame,text='RACE TYPE',fg_color='transparent')
        race_type_button_frame=customtkinter.CTkFrame(master=self.root_left_frame,fg_color='transparent')
        race_buttons=toggle_button.toggle_button(master_frame=race_type_button_frame,
                                   display_texts=['FORMULA RACE','TIME TRIAL'],
                                   default='TIME TRIAL')
        
        racer_type_label=customtkinter.CTkLabel(master=self.root_left_frame,text='PARTICIPANT TYPE',fg_color='transparent')
        racer_type_combobox = customtkinter.CTkComboBox(master=self.root_left_frame, values=["TEAM", "INDIVIDUAL"],
                                     command=self.racer_type_combobox_callback)
        racer_type_combobox.set("SELECT TYPE")
        
        ##RIGHT FRAME
        self.name_table=CTkTable.CTkTable(master=root_right_frame,row=1,column=1,values=[['TEAM NAME']])
        
        #appending frames to the frame list
        frame_list.append(self.root_left_frame)
        frame_list.append(root_right_frame)
        frame_list.append(race_type_button_frame)

        #row and colunm configuring the frames
        root.rowconfigure(0,weight=1)
        root.columnconfigure([0,1],weight=1)
        for i in frame_list:
            col,row=i.grid_size()
            if col!=0:
                col=list(range(col))
            if row!=0:
                row=list(range(row))    
            #i.rowconfigure(row,weight=1)
            i.columnconfigure(col,weight=1)
        
        #grid
        self.root_left_frame.grid(row=0,column=0,sticky='nsew',pady=5)
        root_right_frame.grid(row=0,column=1,sticky='nsew',pady=5)
        ##LEFT FRAME
        race_type_label.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)
        race_type_button_frame.grid(row=0,column=1,sticky='nsew',pady=5)
        racer_type_label.grid(row=1,column=0,sticky='nsew',padx=5,pady=50)
        racer_type_combobox.grid(row=1,column=1,sticky='nsew',padx=5,pady=50)
        
        ##RIGHT FRAME
        self.name_table.grid(row=0,column=0,sticky='nsew',padx=100,pady=10)
        root.mainloop()

    def racer_type_combobox_callback(self,choice):
        
        def check_name(name_widget):
            name=name_widget.get()
            name=name.strip()
            if name=='':
                return
            elif name not in self.team_name_list :
                self.team_name_list.append(name)
                self.name_table.add_row(values=(name,))
                name_widget.delete(0,tkinter.END)
            else:
                tkinter.messagebox.showinfo("ERROR",  'Team "{}" already exits\nPlease Enter a new Team Name'.format(name))    
        
        def remove_name(name_widget):
            name=name_widget.get()
            name=name.strip()
            if name=='':
                return
            elif name in self.team_name_list :
                confirm=tkinter.messagebox.askyesno(title='Remove Team', message="Do You want to remove Team '{}' from the team list ?".format(name))
                if confirm:
                    self.team_name_list.remove(name)

                    self.name_table.delete_row(self.name_table.get().index([name]))
                    name_widget.delete(0,tkinter.END)
                else:
                    name_widget.delete(0,tkinter.END)    
            else:
                tkinter.messagebox.showinfo("ERROR",  'Team "{}" does not exist\nPlease Enter an existing Team Name'.format(name))
                name_widget.delete(0,tkinter.END)
        
        combo_frame=self.root_left_frame
        if choice=='TEAM':
            team_name_label=customtkinter.CTkLabel(master=combo_frame,text='TEAM NAME',fg_color='transparent')
            team_name=customtkinter.CTkEntry(master=self.root_left_frame,fg_color='transparent',placeholder_text='Enter ypur team name')
            btn_frame=customtkinter.CTkFrame(master=combo_frame,fg_color='transparent')
            btn_frame.columnconfigure([0,1],weight=1)
            add_btn=customtkinter.CTkButton(master=btn_frame,text='ADD',command=lambda:check_name(team_name))
            remove_btn=customtkinter.CTkButton(master=btn_frame,text='REMOVE',command=lambda:remove_name(team_name))
            
            team_name_label.grid(row=2,column=0,sticky='nsew',pady=(50,0))
            team_name.grid(row=2,column=1,sticky='ew',pady=(50,0))
            btn_frame.grid(row=3,column=1,sticky='ew')
            add_btn.grid(row=0,column=0,sticky='ew',pady=20,padx=10)
            remove_btn.grid(row=0,column=1,sticky='ew',pady=20,padx=10)


if __name__=="__main__":
    selection_app()        